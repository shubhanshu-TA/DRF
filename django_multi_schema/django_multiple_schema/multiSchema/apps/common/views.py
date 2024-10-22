import structlog
from apps.common.model_class import (
    LanguageSerializer,
    RegionSerializer,
    TenantSerializer,
)
from apps.common.queries import lanreg, tenant
from apps.common.services import (  # add_languages,; update_languages,; delete_languages
    add_languages,
    delete_languages,
    get_languages,
    update_languages,
    get_regions,
    get_tenants,
    get_langregs,
    get_langregs_df,
)
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from generics.exceptions import MissingRequestParamsError
from generics.resp_utils import handle_response
from rest_framework.decorators import APIView
from django.db import connections
from generics.oauth_token_validate import requires_auth

logger = structlog.get_logger(__name__)

class LanguageList(APIView):
    permission_classes = []  # [IsAuthenticated]

    @requires_auth
    @handle_response
    @extend_schema(
        summary="Get the entire list of languages",
        description="API end point that serves the list of languages",
    )
    def get(self, request, **kwargs):
        app_tenant_id = kwargs['auth_data']['app_tenant_id']
        param = request.data or -1
        resp = {}
        logger.bind(
            method_name="get_all_languages", app_name="Common", params=str([-1])
        )
        with connections["common"].cursor() as common_cursor:
            data = get_languages(common_cursor, param, app_tenant_id)
            serializer = LanguageSerializer(data=data, many=True)
            serializer.is_valid()
            resp = serializer.data if serializer.is_valid() else {}
        return resp

    @handle_response
    @extend_schema(
        summary="Add language to list of languages",
        description="API end point to add data to the list of languages",
        parameters=[
            OpenApiParameter(
                name="language_code",
                description="Add by language code",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Add using language code",
                        description="needs language code in URL and add data params in request data",
                        value="ger",
                    )
                ],
            ),
            OpenApiParameter(
                name="language_description",
                description="Add by language description",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Add using language description",
                        description="needs language description in URL and add data params in request data",
                        value="German",
                    )
                ],
            ),
        ],
    )
    def post(self, request):
        post_data = request.data
        serializer = LanguageSerializer(data=post_data)
        logger.bind(method_name="post_languages", app_name="Common", params=post_data)
        if serializer.is_valid():
            with connections["common"].cursor() as common_cursor:
                return add_languages(common_cursor, serializer)
        else:
            raise (MissingRequestParamsError("status", serializer.data))

class LanguageDetail(APIView):
    permission_classes = []  # [IsAuthenticated]
    serializer_class = LanguageSerializer

    @handle_response
    @extend_schema(
        summary="Get the details of a language based on id",
        description="API end point that serves the languages based on language id",
        parameters=[
            OpenApiParameter(
                name="language_id",
                description="Filter by language id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by language id",
                        description="should be an integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        language_id = request.parser_context["kwargs"].get("language_id")
        if not language_id:
            raise MissingRequestParamsError("language id", language_id)
        logger.bind(
            method_name="get_languages", app_name="Common", params=str([language_id])
        )
        with connections["common"].cursor() as common_cursor:
            resp = get_languages(common_cursor, language_id)
            serializer = LanguageSerializer(data=resp, many=True)
            serializer.is_valid()
        return serializer.data if serializer.is_valid() else {}

    @handle_response
    @extend_schema(
        summary="Update a language from list of languages",
        description="API end point that is used to update the list of languages",
        parameters=[
            OpenApiParameter(
                name="language_id",
                description="Update by language id",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Update using language id",
                        description="needs language id in URL and update data params in request data",
                        value=1,
                    )
                ],
            )
        ],
    )
    def put(self, request):
        language_id = request.parser_context["kwargs"].get("language_id")
        if not language_id:
            raise MissingRequestParamsError("language id", language_id)
        logger.bind(
            method_name="put_languages", app_name="Common", params=str([language_id])
        )
        put_data = request.data
        logger.bind(method_name="put_languages", app_name="Common", params=put_data)
        with connections["common"].cursor() as common_cursor:
            item = get_languages(common_cursor, language_id)
            serializer = LanguageSerializer(put_data, data=item[0], partial=True)

            if serializer.is_valid():
                update_languages(common_cursor, language_id, put_data)
                return {"status": "data updated succesfully"}
            else:
                raise MissingRequestParamsError("status", "data")

    @handle_response
    @extend_schema(
        summary="Delete a language",
        description="API end point that is used to delete a language",
        parameters=[
            OpenApiParameter(
                name="language_id",
                description="delete using the language id",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="delete using the language id",
                        description="language id is needed to delete a language",
                        value=1,
                    )
                ],
            )
        ],
    )
    def delete(self, request):
        language_id = request.parser_context["kwargs"].get("language_id")
        if not language_id:
            raise MissingRequestParamsError("language id", language_id)
        logger.bind(
            method_name="delete_languages", app_name="Common", params=language_id
        )
        with connections["common"].cursor() as common_cursor:
            item = get_languages(common_cursor, language_id)
            serializer = LanguageSerializer(data=item[0])

            if serializer.is_valid():
                delete_languages(common_cursor, language_id)
                return {"status": "data deleted succesfully"}
            else:
                raise MissingRequestParamsError("status", "data")

class RegionDetail(APIView):
    permission_classes = []  # [IsAuthenticated]
    serializer_class = RegionSerializer

    @handle_response
    @extend_schema(
        summary="Get the details of a region based on id",
        description="API end point that serves the regions based on region id",
        parameters=[
            OpenApiParameter(
                name="region_id",
                description="Filter by region id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by region id",
                        description="should be an integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        region_id = request.parser_context["kwargs"].get("region_id")
        if not region_id:
            raise MissingRequestParamsError("region id", region_id)
        logger.bind(
            method_name="get_regions", app_name="Common", params=str([region_id])
        )
        with connections["common"].cursor() as common_cursor:
            resp = get_regions(common_cursor, region_id)
            serializer = RegionSerializer(data=resp, many=True)
            serializer.is_valid()
        return serializer.data if serializer.is_valid() else {}

class LanRegDetail(APIView):
    permission_classes = []  # [IsAuthenticated]

    @handle_response
    @extend_schema(
        summary="Get the details from the language table after filtering on region id",
        description="API end point that serves the region and language tables combined",
        parameters=[
            OpenApiParameter(
                name="region_id",
                description="Filter by region id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by region id",
                        description="should be an integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        result = {}
        region_id = request.parser_context["kwargs"].get("region_id")
        if not region_id:
            raise MissingRequestParamsError("region id", region_id)
        logger.bind(
            method_name="get_lanreg", app_name="Common", params=str([region_id])
        )
        with connections["common"].cursor() as common_cursor:
            result = get_langregs(common_cursor, [region_id])
        return result

class TenantDetail(APIView):
    permission_classes = []  # [IsAuthenticated]

    @handle_response
    @extend_schema(
        summary="Get the details of a language based on tenant_id",
        description="API end point that serves the languages based on tenant_id",
        parameters=[
            OpenApiParameter(
                name="tenant_id",
                description="Filter by tenant id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by tenant id",
                        description="should be an integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        tenant_id = request.parser_context["kwargs"].get("tenant_id")
        if not tenant_id:
            raise MissingRequestParamsError("tenant id", tenant_id)
        logger.bind(
            method_name="get_tenant_languages",
            app_name="Common",
            params=str([tenant_id]),
        )
        with connections["common"].cursor() as common_cursor:
            resp = get_tenants(common_cursor, tenant_id)
            serializer = TenantSerializer(data=resp, many=True)
            serializer.is_valid()
        return serializer.data if serializer.is_valid() else {}

class LanRegDfDetail(APIView):
    permission_classes = []  # [IsAuthenticated]

    @handle_response
    @extend_schema(
        summary="Get the details from the language table after filtering on region id",
        description="API end point that serves the region and language tables combined",
        parameters=[
            OpenApiParameter(
                name="region_id",
                description="Filter by region id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by region id",
                        description="should be an integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        result = {}
        region_id = request.parser_context["kwargs"].get("region_id")
        if not region_id:
            raise MissingRequestParamsError("region id", region_id)
        logger.bind(
            method_name="get_lanreg_df", app_name="Common", params=str([region_id])
        )
        with connections["common"].cursor() as common_cursor:
            result = get_langregs_df(common_cursor, [region_id])
        return result
    