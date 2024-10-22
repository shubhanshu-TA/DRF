import datetime
import logging
from dataclasses import dataclass, field

from apps.common.model_class import Language
from apps.common.queries import fixedPromos, usergoes
from generics.exceptions import EmptyObjectError, MissingRequestParamsError, NoDataError
from generics.repository import ModelRepository
from generics.unit_of_work import AbstractUnitOfWork, ORMModelUnitOfWork
from rest_framework import serializers

logger = logging.getLogger(__name__)


def get_languages(cur, param):
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
        resp = repo_obj.getAll()
    elif param >= 0:
        resp = repo_obj.get([param])
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
