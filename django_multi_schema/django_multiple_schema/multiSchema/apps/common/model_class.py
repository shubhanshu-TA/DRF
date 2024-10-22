from __future__ import annotations

import datetime
from dataclasses import dataclass, field, fields
from typing import Optional
from django.db import models

# dataclass for languages
from django_dataclass_autoserialize import AutoSerialize, DataclassSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from generics.models import Tenant, TimeStampModel, TenantAwareModel


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
    tenant_id: int
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
            tenant_id=1,
            default_language="en",
            id=1,
            created_by="user",
            modified_by="user",
        )


class LanguageSerializer(DataclassSerializer):
    class Meta:
        dataclass = Language


@dataclass
class Region(AutoSerialize):
    # id: int = field(init=False)
    region_name: str
    region_code: str
    active: int
    created_by: str
    modified_by: str
    created_at: datetime.datetime = field(default=datetime.datetime.now())
    modified_at: datetime.datetime = field(default=datetime.datetime.now())

    __table__ = "regions"

    def __post_init__(self):
        validate(self)

    @classmethod
    def example(cls) -> Region:
        # this is actually optional but it will show up
        # in swagger doc
        return cls(
            region_name="sample",
            region_code="rc_1",
            active=True,
            created_by="user",
            modified_by="user",
        )


class RegionSerializer(DataclassSerializer):
    class Meta:
        dataclass = Region


class TenantSerializer(DataclassSerializer):
    class Meta:
        dataclass = Tenant



