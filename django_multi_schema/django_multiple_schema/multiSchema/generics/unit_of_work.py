from __future__ import annotations
import abc
import pandas as pd


class AbstractUnitOfWork(abc.ABC):
    def __init__(self, conn, trans) -> AbstractUnitOfWork:
        self.connection = conn
        self.transaction = trans

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class ORMModelUnitOfWork(AbstractUnitOfWork):
    def __init__(self, transaction, repository_object):
        self.repoObj = repository_object()
        self.transaction = transaction

    def __enter__(self):
        self.auto_commit_orig = self.transaction.get_autocommit()
        self.transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.transaction.set_autocommit(self.auto_commit_orig)

    def commit(self):
        self.transaction.commit()

    def rollback(self):
        self.transaction.rollback()

    def filter_by_id(self, id=None):
        return self.repoObj.get(id)

    def raw_queryset_as_values_list(self, raw_qs):
        columns = raw_qs.columns
        for row in raw_qs:
            yield tuple(getattr(row, col) for col in columns)

    def get_data_df(self, query_string, params):
        results = self.repoObj._model.raw(query_string, params)
        return pd.DataFrame(
            self.raw_queryset_as_values_list(results), columns=list(results.columns)
        )

    def get_raw_query_data(self, query_string, params):
        # return data as list of dicts
        results = self.repoObj._model.raw(query_string, params)
        columns = results.columns
        return [
            dict(tuple((col, getattr(row, col)) for col in columns)) for row in results
        ]

    def filter_by_language_code(self, language_codes=()):
        return self.repoObj._model.filter(language_code__in=language_codes)
