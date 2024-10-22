from django_dataclass_autoserialize import AutoSerialize
from dataclasses import dataclass, fields, field
import datetime
from typing import Optional


def validate(instance):
    for field in fields(instance):
        attr = getattr(instance, field.name)
        if not isinstance(attr, field.type):
            msg = "Field {0.name} is of type {1}, should be {0.type}".format(
                field, type(attr)
            )
            raise ValueError(msg)


@dataclass
class Language(AutoSerialize):
    id: int = field(init=False)
    language_code: str
    language_description: str
    active: bool
    created_by: str
    modified_by: str
    default_language: str
    region_id: int
    created_at: datetime.datetime = field(default=datetime.datetime.now())
    modified_at: datetime.datetime = field(default=datetime.datetime.now())

    __table__ = "languages"

    def __post_init__(self):
        validate(self)

    @classmethod
    def example(cls) -> Language:
        # this is actually optional but it will show up
        # in swagger doc
        return cls(a=3, b=2)

    def get_data_by_id(self, id):
        return "select * from {table} where id={id}".format(table=self.__table__, id=id)

    def get_all_data(self):
        return "select * from {table}".format(table=self.__table__)

    def post_data(
        self,
    ):
        return "select * from {table} where id={id}".format(table=self.__table__, id=id)

    def get_data_by_id(self, id):
        return "select * from {table} where id={id}".format(table=self.__table__, id=id)


@dataclass
class Numbers(Validations):
    a: int
    __table__ = "MyTable"

    def __post_init__(self):
        validate(self)
