from __future__ import annotations

import datetime
from dataclasses import dataclass, field, fields
from typing import Optional

# dataclass for languages
from django_dataclass_autoserialize import AutoSerialize, DataclassSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


def validate(instance):
    for field in fields(instance):
        attr = getattr(instance, field.name)
        if "_MISSING_TYPE" not in field.default.__str__() and isinstance(
            type(attr), type
        ):
            attr = field.default
        if not isinstance(attr, eval(field.type)):
            msg = "Field {0.name} is of type {1}, should be {0.type}".format(
                field, type(attr)
            )
            raise ValueError(msg)


@dataclass
class Language(AutoSerialize):
    # id: int = field(init=False)
    language_code: str
    language_description: str
    currency_symbol: str
    active: int
    created_by: str
    modified_by: str
    default_language: str
    region_id: int
    created_at: datetime.datetime = field(default=datetime.datetime.now())
    modified_at: datetime.datetime = field(default=datetime.datetime.now())

    __table__ = "language_new"

    def __post_init__(self):
        validate(self)

    @classmethod
    def example(cls) -> Language:
        # this is actually optional but it will show up
        # in swagger doc
        return cls(
            language_code="en",
            language_description="english",
            active=True,
            region_id=1,
            default_language="en",
            id=1,
            created_by="user",
            modified_by="user",
        )


class LanguageSerializer(DataclassSerializer):
    class Meta:
        dataclass = Language


# class AddView(APIView):

#     @extend_schema(
#         body_type=Language,
#         response_types={200: ComputeResponse}
#     )
#     def post(self, request: Request) -> Response:
#         param = Language.from_post_request(request)
#         return ComputeResponse(msg='add successfully',
#                                result=param.a + param.b).to_response()

#     @extend_schema(
#         query_type=Language,
#         response_types={200: ComputeResponse}
#     )
#     def get(self, request: Request) -> Response:
#         param = LanguageSerializer.from_get_request(request)
#         return ComputeResponse(msg='subtract successfully',
#                                result=param.a - param.b).to_response()
