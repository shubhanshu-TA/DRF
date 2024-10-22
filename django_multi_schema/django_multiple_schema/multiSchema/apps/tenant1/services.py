import logging
from generics.unit_of_work import AbstractUnitOfWork
from generics.exceptions import (
    MissingRequestParamsError,
    NoDataError,
    EmptyObjectError,
)
from rest_framework import serializers
from apps.common.queries import usergoes, fixedPromos
from dataclasses import dataclass, field
import datetime
from apps.common.model_class import Language
from generics.unit_of_work import ORMModelUnitOfWork
from generics.repository import ModelRepository

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
