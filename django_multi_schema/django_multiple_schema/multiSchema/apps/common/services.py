import datetime
import logging
from dataclasses import dataclass, field

from apps.common.model_class import Language, Region, Tenant
from generics.exceptions import EmptyObjectError, MissingRequestParamsError, NoDataError
from generics.repository import ModelRepository
from apps.common.queries import lanreg

logger = logging.getLogger(__name__)


def get_languages(cur, param, tenant_id):
    """Return the list of languages

    Parameters
    ----------
    cursor
        To connect to the right database
    param
        To filter data based on user preferences

    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    repo_obj = ModelRepository(Language, cur)
    if param == -1:
        resp = repo_obj.getAll(tenant_id)
    elif param >= 0:
        resp = repo_obj.get(param, tenant_id)
    else:
        raise MissingRequestParamsError("Not a valid parameter %s" % param)
    if not resp:
        raise NoDataError("language id %s" % (param))
    return resp


def add_languages(cur, param):
    """Add to the list of languages

    Parameters
    ----------
    cursor
        To connect to the right database
    param
        To filter data based on user preferences

    Returns
    -------
    Success of Failure

    """
    resp = {}
    repo_obj = ModelRepository(Language, cur)
    resp = repo_obj.add(param)
    if not resp:
        raise NoDataError("language id %s" % (param))
    return resp


def update_languages(cur, id, param):
    """Update a language in a list of languages

    Parameters
    ----------
    cursor
        To connect to the right database
    id
        To update data of that particular row
    param
        To update the columns based on data
    Returns
    -------
        Success of Failure

    """
    resp = {}
    repo_obj = ModelRepository(Language, cur)
    resp = repo_obj.update(id, param)
    if not resp:
        raise NoDataError("language id %s" % (id))
    return resp


def delete_languages(cur, id):
    """Delte a language in a list of languages

    Parameters
    ----------
    cursor
        To connect to the right database
    id
        To update data of that particular row
    Returns
    -------
        Success of Failure

    """
    resp = {}
    repo_obj = ModelRepository(Language, cur)
    resp = repo_obj.delete([id])
    if not resp:
        raise NoDataError("language id %s" % (id))
    return resp


def get_regions(cur, param):
    """Return the list of regions

    Parameters
    ----------
    cursor
        To connect to the right database
    param
        To filter data based on user preferences

    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    repo_obj = ModelRepository(Region, cur)
    if param == -1:
        resp = repo_obj.getAll()
    elif int(param) >= 0:
        resp = repo_obj.get([param])
    else:
        raise MissingRequestParamsError("Not a valid parameter %s" % param)
    if not resp:
        raise NoDataError("region id %s" % (param))
    return resp


def get_tenants(cur, param):
    """Return the list of regions

    Parameters
    ----------
    cursor
        To connect to the right database
    param
        To filter data based on user preferences

    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    repo_obj = ModelRepository(Tenant, cur)
    if param == -1:
        resp = repo_obj.getAll()
    elif int(param) >= 0:
        resp = repo_obj.get([param])
    else:
        raise MissingRequestParamsError("Not a valid parameter %s" % param)
    if not resp:
        raise NoDataError("region id %s" % (param))
    return resp


def get_langregs(cur, param):
    """Return the mapped list of regions & languages

    Parameters
    ----------
    cursor
        To connect to the right database
    param
        To filter data based on region id

    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    repo_obj = ModelRepository(Language, cur)
    if param:
        resp = repo_obj.get_raw_query_data(lanreg(), param)
    else:
        raise MissingRequestParamsError("Not a valid parameter %s" % param)
    if not resp:
        raise NoDataError("region id %s" % (param))
    return resp


def get_langregs_df(cur, param):
    """Return the mapped list of regions & languages

    Parameters
    ----------
    cursor
        To connect to the right database
    param
        To filter data based on region id

    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    repo_obj = ModelRepository(Language, cur)
    if param:
        resp_df = repo_obj.get_data_df(lanreg(), param)
        # filtering the data from the df and converting it into a dict
        resp_df = resp_df[resp_df["language_code"].apply(lambda x: x == "hind")]
        resp = resp_df.to_dict(orient="records")
    else:
        raise MissingRequestParamsError("Not a valid parameter %s" % param)
    if not resp:
        raise NoDataError("region id %s" % (param))
    return resp
