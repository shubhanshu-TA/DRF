from os import stat
import json
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
import structlog
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from apps.tenant1.services import (
    get_languages,
    # add_languages,
    # update_languages,
    # delete_languages
)
from rest_framework.decorators import APIView
from generics.resp_utils import handle_response
from generics.exceptions import MissingRequestParamsError
from datetime import datetime
import pandas as pd
from apps.tenant1.services import (
    get_languages,
    add_languages,
    update_languages,
    delete_languages,
)
from apps.tenant1.model_class import LanguageSerializer
from django.db import connections

logger = structlog.get_logger(__name__)

tenant1_cursor = connections["tenant1"].cursor()


class LanguageList(APIView):
    permission_classes = []  # [IsAuthenticated]

    @handle_response
    @extend_schema(
        summary="Get the entire list of languages",
        description="API end point that serves the list of languages",
    )
    def get(self, request):
        param = request.data or -1
        resp = {}
        logger.bind(
            method_name="get_all_languages", app_name="tenant1", params=str([-1])
        )
        with connections["tenant1"].cursor() as ten1_cursor:
            data = get_languages(ten1_cursor, param)
            serializer = LanguageSerializer(data=data, many=True)
            serializer.is_valid()
            resp = serializer.data if serializer.is_valid() else {}
        return resp

    @handle_response
    @extend_schema(
        summary="Add language to list of languages",
        description="API end point to add data to the list of languages",
    )
    def post(self, request):
        post_data = request.data
        serializer = LanguageSerializer(data=post_data)
        logger.bind(method_name="post_languages", app_name="tenant1", params=post_data)
        if serializer.is_valid():
            return add_languages(tenant1_cursor, serializer)
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
                        description="should be a integer value",
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
            method_name="get_languages", app_name="tenant1", params=str([language_id])
        )
        resp = get_languages(tenant1_cursor, language_id)
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
            method_name="put_languages", app_name="tenant1", params=str([language_id])
        )
        put_data = request.data
        item = get_languages(tenant1_cursor, language_id)
        serializer = LanguageSerializer(put_data, data=item[0], partial=True)
        logger.bind(method_name="put_languages", app_name="tenant1", params=put_data)
        if serializer.is_valid():
            update_languages(tenant1_cursor, language_id, put_data)
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
        item = get_languages(tenant1_cursor, language_id)
        serializer = LanguageSerializer(data=item[0])
        logger.bind(method_name="put_languages", app_name="tenant1", params=language_id)
        if serializer.is_valid():
            delete_languages(tenant1_cursor, language_id)
            return {"status": "data deleted succesfully"}
        else:
            raise MissingRequestParamsError("status", "data")
