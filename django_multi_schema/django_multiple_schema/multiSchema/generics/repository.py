from abc import ABC, abstractmethod

import pandas as pd
from rest_framework.serializers import ValidationError


class AbstractRepository(ABC):
    """Abstracts the notion of an object/entity store."""

    def __init__(self, uow_man):
        self.uow = uow_man

    @abstractmethod
    def add(self, entity):
        """Insert a new entity into the data store."""
        raise NotImplementedError("add")

    @abstractmethod
    def delete(self, id):
        """Remove a persistent entity from the datastore."""
        raise NotImplementedError("delete")

    @abstractmethod
    def get(self, id):
        """Fetch an entity from the datastore by its identifier."""
        raise NotImplementedError("get")

    @abstractmethod
    def getAll(self):
        """Fetch an entity from the datastore by its identifier."""
        raise NotImplementedError("get")

    @abstractmethod
    def update(self, id):
        """Update an entity in the datastore by its identifier."""
        raise NotImplementedError("update")


class ModelRepository(AbstractRepository):
    def __init__(self, model_class, cursor):
        self.model_class = model_class
        self.table_name = model_class.__table__
        self.fields = model_class.fields
        self.cursor = cursor

    def add(self, data):
        columns = ",".join([i for i in data.fields])
        value_list, value_str_list = [],[]
        for col in data:
            value_str_list.append('"%s"' if isinstance(col.value, str) else "%s")
            value_list.append(col.value)
        
        query = "insert into {table} ({columns}) values ".format(
            table=self.table_name, columns=columns
        )
        query += "("+','.join(value_str_list)+")"
        self.cursor.execute(query, value_list)
        return {"msg": "Added Successfully"}

    def get(self, params, tenant_id):
        query = "select * from {table} where id=%s and active=1 and tenant_id in {tenant_ids}".format(
            table=self.table_name, tenant_ids = tenant_id
        )
        data = self.cursor.execute(query, [params])
        col_names = [field[0] for field in data.description]
        response = [dict(zip(col_names, row)) for row in data]
        return response

    def getAll(self, tenant_id):
        query = "select * from {table} where active=1 and tenant_id in {tenant_ids}".format(table=self.table_name, tenant_ids = tenant_id)
        data = self.cursor.execute(query)
        col_names = [field[0] for field in data.description]
        response = [dict(zip(col_names, row)) for row in data]
        return response

    def update(self, uid, data):
        column_list, value_list = [], []
        for k, v in data.items():
            column_list.append(k + '="%s"' if isinstance(v, str) else k + "=%s")
            value_list.append(v)
        query = "update {table} set {columns} where id=%s".format(
            table=self.table_name, columns=', '.join(column_list)
        )
        self.cursor.execute(query, value_list+[uid])
        return {"msg": "Updated Successfully"}

    def delete(self, params):
        query = "delete from {table} where id=%s".format(
            table=self.table_name
        )
        self.cursor.execute(query, params)
        return {"msg": "Deleted Successfully"}

    def get_data_df(self, query_string, params):
        results = self.cursor.execute(query_string, params)
        df = pd.DataFrame(
            [row for row in results],
            columns=[field[0] for field in results.description],
        )
        return df

    def get_raw_query_data(self, query, params):
        # return data as dataframe
        data = self.cursor.execute(query, params)
        col_names = [field[0] for field in data.description]
        response = [dict(zip(col_names, row)) for row in data]
        return response
