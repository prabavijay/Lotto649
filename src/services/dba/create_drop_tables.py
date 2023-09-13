from src.services.dba.db_connect import DbConnect
from src.services.dba.db_model import (DrawResults, DrawStats, Subsequence, Tickets)


def get_list_of_tables():
    tables = []
    tables.extend([DrawResults.__table__, DrawStats.__table__,
                   Subsequence.__table__, Tickets.__table__])
    return tables


class TableCreateDrop(DbConnect):

    def __init__(self):
        super().__init__()
        self.tables_list = get_list_of_tables()

    def drop_table(self, table_name):
        self.base.metadata.drop_all(self.engine, tables=[table_name])

    def drop_tables(self):
        self.base.metadata.drop_all(self.engine, tables=self.tables_list)

    def create_table(self, table_name):
        self.base.metadata.create_all(self.engine, tables=[table_name])

    def create_tables(self):
        self.base.metadata.create_all(self.engine, tables=self.tables_list)

    def delete_rows(self, table_class):
        self.session.query(table_class).delete()
