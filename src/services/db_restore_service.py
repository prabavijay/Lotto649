"""
DBRestoreService - service class to handle restoring DB (including recreating tables).
"""
from src.services.dba.db_model import (DrawResults, DrawStats, Tickets, Subsequence)
from src.services.dba.db_model import (FreqByBall, FreqByDay, FreqByDate, FreqByMonth, Repetition, FreqAndMissing)


# provides list of table names
def get_list_of_tables():
    tables = []
    tables.extend([DrawResults.__tablename__, DrawStats.__tablename__, Tickets.__tablename__,
                   Subsequence.__tablename__, Repetition.__tablename__, FreqAndMissing.__tablename__])
    return tables


def get_list_of_tables_new():
    tables = []
    tables.extend([FreqByBall.__tablename__, FreqByDay.__tablename__, FreqByDate.__tablename__, FreqByMonth.__tablename__])
    return tables


class DBRestoreService:

    def __init__(self, db_connect):
        print("in 10 - DBRestoreService")
        self.engine = db_connect.engine
        self.session = db_connect.session
        self.base = db_connect.base
        self.tables_list = get_list_of_tables()
        self.tables_list_new = get_list_of_tables_new()

    def drop_tables(self):
        self.base.metadata.drop_all(self.engine, tables=self.tables_list)

    def create_tables(self):
        self.base.metadata.create_all(self.engine, tables=self.tables_list)

    def create_tables_new(self):
        self.base.metadata.drop_all(self.engine, tables=self.tables_list_new)
        self.base.metadata.create_all(self.engine, tables=self.tables_list_new)

    def setup_table_with_49rows(self, table_class):
        # this method inserts 49 rows into table for 'drawn_number' column which is also primary_key
        # table only meant to have 49 rows
        for i in range(1, 50):
            row = None  # here i is the drawn_number
            if table_class == FreqByBall:
                row = table_class(i)  # here i is the drawn_number
            elif table_class == FreqByDay:
                row = table_class(i, 0, 0)  # here i is the drawn_number
            elif table_class == FreqByDate:
                row = table_class(i)  # here i is the drawn_number
            elif table_class == FreqByMonth:
                row = table_class(i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # here i is the drawn_number
            self.session.add(row)
        self.session.commit()

    def delete_rows(self, table_class):
        if table_class == "DrawResults":
            table_class = DrawResults
        self.session.query(table_class).delete()
