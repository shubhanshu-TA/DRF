import os
from functools import wraps
import string
from dotenv import load_dotenv
from django.http import HttpResponse, HttpRequest
import jwt
import requests
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from .models import Tenant

tenant_id = os.environ.get("AZ_TENANT", "e714ef31-faab-41d2-9f1e-e6df4af16ab8")
client_id = os.environ.get("AZ_CLIENT_ID", "9ffb6d74-96a4-4890-a0f1-0fdd7baa428f")

b2c_policy_name = None
b2c_domain_name = None


try:
    ENV_MRK = os.environ.get("ENV_MRK", "0")
    if ENV_MRK == "0":
        dotenv_path = os.path.join(os.getcwd(), os.environ.get("ENV")) + ".env"
        load_dotenv(dotenv_path)
except Exception as exception:
    pass


class AuthError(Exception):
    def __init__(self, error_msg: str, status: int):
        super().__init__(error_msg)

        self.error_msg = error_msg
        self.status = status


def ensure_bytes(key):
    if isinstance(key, str):
        key = key.encode("utf-8")
    return key


def decode_value(val):
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b"==")
    return int.from_bytes(decoded, "big")


def rsa_pem_from_jwk(jwk):
    return (
        RSAPublicNumbers(n=decode_value(jwk["n"]), e=decode_value(jwk["e"]))
        .public_key(default_backend())
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def get_token_auth_header(request: HttpRequest):
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError("Authentication error: Authorization header is missing", 401)

    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            "Authentication error: Authorization header must start with ' Bearer'", 401
        )
    elif len(parts) == 1:
        raise AuthError("Authentication error: Token not found", 401)
    elif len(parts) > 2:
        raise AuthError(
            "Authentication error: Authorization header must be 'Bearer <token>'", 401
        )

    token = parts[1]
    return token


def decode_b2c_jwt(token_version, token, rsa_key, alg):
    if token_version == "1.0":
        _issuer = f"https://{b2c_domain_name}.b2clogin.com/tfp/{tenant_id}/{b2c_policy_name}/v2.0/".lower()
    else:
        _issuer = f"https://{b2c_domain_name}.b2clogin.com/{tenant_id}/v2.0".lower()
    try:
        payload = jwt.decode(
            token, rsa_key, algorithms=[alg], audience=client_id, issuer=_issuer
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("Token error: The token has expired", 401)
    except Exception:
        raise AuthError("Token error: Unable to parse authentication", 401)


def __decode_jwt(token_version, token, rsa_key, alg):
    if token_version == "1.0":
        _issuer = f"https://sts.windows.net/{tenant_id}/"
        _audience = f"api://{client_id}"
    else:
        _issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        _audience = f"{client_id}"
    try:
        payload = jwt.decode(
            token,
            rsa_pem_from_jwk(rsa_key),
            algorithms=[alg],
            audience=_audience,
            issuer=_issuer,
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("Token error: The token has expired", 401)
    except Exception:
        raise AuthError("Token error: Unable to parse authentication", 401)


def __get_token_version(token, alg):
    unverified_claims = jwt.decode(
        token, algorithms=[alg], options={"verify_signature": False},
        audience = client_id
    )
    if unverified_claims.get("ver"):
        return unverified_claims["ver"]
    else:
        raise AuthError("Missing version claim from token. Unable to validate", 403)


def get_token_claims(request: HttpRequest, alg: string):
    token = get_token_auth_header(request)
    unverified_claims = jwt.decode(
        token, algorithms=[alg], options={"verify_signature": False}
    )
    return unverified_claims


def validate_scope(required_scope: str, request: HttpRequest, alg: string):
    has_valid_scope = False
    token = get_token_auth_header(request)
    unverified_claims = jwt.decode(
        token, algorithms=[alg], options={"verify_signature": False}
    )

    ## check to ensure that either a valid scope or a role is present in the token
    if unverified_claims.get("scp") is None and unverified_claims.get("roles") is None:
        raise AuthError(
            "IDW10201: No scope or app permission (role) claim was found in the bearer token",
            403,
        )

    is_app_permission = True if unverified_claims.get("roles") is not None else False

    if is_app_permission:
        if unverified_claims.get("roles"):
            # the roles claim is an array
            for scope in unverified_claims["roles"]:
                if scope.lower() == required_scope.lower():
                    has_valid_scope = True
        else:
            raise AuthError(
                "IDW10201: No app permissions (role) claim was found in the bearer token",
                403,
            )
    else:
        if unverified_claims.get("scp"):
            # the scp claim is a space delimited string
            token_scopes = unverified_claims["scp"].split()
            for token_scope in token_scopes:
                if token_scope.lower() == required_scope.lower():
                    has_valid_scope = True
        else:
            raise AuthError(
                "IDW10201: No scope claim was found in the bearer token", 403
            )

    if is_app_permission and not has_valid_scope:
        raise AuthError(
            f'IDW10203: The "role" claim does not contain role {required_scope} or was not found',
            403,
        )
    elif not has_valid_scope:
        raise AuthError(
            f'IDW10203: The "scope" or "scp" claim does not contain scopes {required_scope} or was not found',
            403,
        )


def get_rsa_key(tenant_id: string, token: string):
    rsa_key = {}
    alg = ""
    try:
        url = f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
        resp = requests.get(url, timeout=None)
        if resp.status_code != 200:
            raise AuthError("Problem with Azure AD discovery URL", status=404)
        jwks = resp.json()
        unverified_header = jwt.get_unverified_header(token)
        alg = unverified_header["alg"]
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

    except Exception as error:
        return HttpResponse(
            content="Invalid_header: Unable to parse authentication", status=401
        )
    return rsa_key, alg

def tenant_from_roles(roles):
    data = Tenant.objects.filter(name__in = roles).all()
    return tuple([i.id for i in data])

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_token_auth_header(args[1])
            rsa_key, alg = get_rsa_key(tenant_id, token)
            if rsa_key:
                try:
                    token_version = __get_token_version(token, alg)
                    payload = __decode_jwt(token_version, token, rsa_key, alg)
                    roles = payload.get('roles', [])
                    
                    if not roles:
                        raise AuthError
                    else:
                        roles = tenant_from_roles(roles)
                        payload['app_tenant_id'] = roles
                    kwargs["auth_data"] = payload
                    return f(*args, **kwargs)
                except AuthError as auth_err:
                    HttpResponse(content=auth_err.error_msg, status=auth_err.status)
                    return HttpResponse(
                        content="Invalid header error: Unable to find appropriate key",
                        status=401,
                    )
        except Exception as e:
            return HttpResponse(
                content="Invalid_header: Unable to parse authentication", status=401
            )

    return decorated


def requires_b2c_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            token = get_token_auth_header(kwargs["request"])
            url = f"https://{b2c_domain_name}.b2clogin.com/{b2c_domain_name}.onmicrosoft.com/{b2c_policy_name}/discovery/v2.0/keys"
            async with requests as client:
                resp: HttpResponse = await client.get(url, timeout=None)
                if resp.status != 200:
                    raise AuthError("Problem with Azure AD discovery URL", status=404)

                jwks = resp.json()
                unverified_header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        rsa_key = {
                            "kid": key["kid"],
                            "kty": key["kty"],
                            "n": key["n"],
                            "e": key["e"],
                            "nbf": key["nbf"],
                        }
        except Exception:
            return HttpResponse(
                content="Invalid_header: Unable to parse authentication", status=401
            )
        if rsa_key:
            try:
                token_version = __get_token_version(token)
                decode_b2c_jwt(token_version, token, rsa_key)
                return await f(*args, **kwargs)
            except AuthError as auth_err:
                HttpResponse(content=auth_err.error_msg, status=auth_err.status)
        return HttpResponse(
            content="Invalid header error: Unable to find appropriate key", status=401
        )

    return decorated
