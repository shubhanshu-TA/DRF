import logging
from enum import Enum
from django.http import HttpResponse
import functools
import json
import structlog
from django.shortcuts import HttpResponse
from generics.exceptions import NoDataError, MissingRequestParamsError, EmptyObjectError
from rest_framework import serializers

logger = structlog.get_logger(__name__)


logger = logging.getLogger(__name__)


class StatusEnum(Enum):
    """
    Status class is used for get statuses
    """

    Saved = 1
    Submmitted = 2
    Completed = 3
    OfferPackageId = 1000
    Scenario = 2
    Discount = 1
    ObjectiveDefault = 1
    ImpactIndex = 0
    ScenarioOverallMetric = "overall"
    ScenarioOverallMetricValue = "channel"
    Segments = "1001"
    ProductCategory = "1002"
    DefaultMetricCode = "1007"
    Flag = 1


def log_activity_info(module, page_name, action):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(self):
            result = func(self)
            logger.info(self.request, module, page_name, action)
            return result

        return wrapper

    return actual_decorator


def validate_input_parameters(func):
    def wrapper(*args, **kwargs):
        params = locals()
        for _item in params:
            if _item == "category":
                if not params[_item] or params[_item] not in (
                    "segments",
                    "products",
                    "overall",
                ):
                    raise MissingRequestParamsError(_item, params[_item])
            elif _item == "scenario_ids":
                if not params[_item] or not isinstance(params[_item], list):
                    raise MissingRequestParamsError(_item, params[_item])
        return func(*args, **kwargs)

    return wrapper


def handle_response(func):
    def wrapper(*args, **kwargs):
        response = {"data": "", "status": "OK", "http_code": 200}
        try:
            #request = args[1]
            #validate the oauth token from the args
            #if the token is valid then return the tenant id as response
            #if the token is not valid then return False
            #the recevied tenant id can be passed to the function
            result = func(*args, **kwargs)
            response["data"] = result
        except MissingRequestParamsError as error:
            logger.exception(str(error))
            response = {
                "data": error.__str__(),
                "status": "ERROR IN PARAMS",
                "http_code": 406,
            }
        except NoDataError as error:
            logger.exception(str(error))
            response = {
                "data": error.__str__(),
                "status": "NO DATA FOUND",
                "http_code": 404,
            }
        except EmptyObjectError as error:
            logger.exception(str(error))
            response = {
                "data": [],
                "status": "NO DATA FOUND",
                "http_code": 404,
            }
        except serializers.ValidationError as error:
            logger.exception(str(error.default_detail))
            response = {
                "data": str(error.default_detail),
                "status": "Data not accepted",
                "http_code": error.status_code,
            }
        except Exception as error:
            logger.exception(str(error))
            response = {
                "data": "INTERNAL SERVER ERROR",
                "status": "ERROR",
                "http_code": 500,
            }
        return HttpResponse(
            json.dumps(response),
            content_type="Application/json",
            status=int(response["http_code"]),
        )

    return wrapper
