"""
DbConnect - to configure, create, connection to Postgres DB

NOTE 1:     Commands to check Status, Start, Stop
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo systemctl stop postgresql
PgAdmin Tool: For Desktop tool Admin User Password is 'ab####cd'

NOTE 2: SQL codes for Database: kenodb

-- DROP DATABASE IF EXISTS kenodb;

CREATE DATABASE kenodb
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_CA.UTF-8'
    LC_CTYPE = 'en_CA.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT TEMPORARY, CONNECT ON DATABASE kenodb TO PUBLIC;

GRANT ALL ON DATABASE kenodb TO kenouser;

GRANT ALL ON DATABASE kenodb TO postgres;

NOTE 3: SQLAlchemy

"""
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import text
from psycopg2 import connect, Error
from src.utils import sql_result_to_list

HOST = "localhost"
DB = "l649db"
USER = "l649user"
PASSWORD = "oknow2023"

print(f"SQLAlchemy version: {sqlalchemy.__version__}")

class DbConnect:

    def __init__(self):
        # print("in 11 - DbConnect")
        self.engine = self.create_engine()
        self.conn = self.create_connection()
        self.session = Session(self.engine)
        self.base = self.get_base()
        # self._cursor =

    @staticmethod
    def create_engine():
        """Create engine which will be bind to database"""
        url = "postgresql+psycopg2://"
        url = url + USER + ":"
        url = url + PASSWORD + "@"
        url = url + HOST + "/"
        url = url + DB
        engine = create_engine(url, echo=False)
        return engine

    def create_connection(self):
        """Create database connection."""
        return self.engine.connect()

    def get_base(self):
        Base = automap_base()
        Base.prepare(autoload_with=self.engine)
        return Base

    def print_url(self):
        print("DB URL: ", self.engine.url)

    def run_sql_statement(self, sql_statement):
        with self.engine.connect() as conn:
            result_raw = conn.execute(text(sql_statement))
            result = sql_result_to_list(result_raw) # converting raw result type to list
        return result


# class Database:
#     def __init__(self, name):
#         self._conn = sqlite3.connect(name)
#         self._cursor = self._conn.cursor()
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.close()
#
#     @property
#     def connection(self):
#         return self._conn
#
#     @property
#     def cursor(self):
#         return self._cursor
#
#     def commit(self):
#         self.connection.commit()
#
#     def close(self, commit=True):
#         if commit:
#             self.commit()
#         self.connection.close()
#
#     def execute(self, sql, params=None):
#         self.cursor.execute(sql, params or ())
#
#     def fetchall(self):
#         return self.cursor.fetchall()
#
#     def fetchone(self):
#         return self.cursor.fetchone()
#
#     def query(self, sql, params=None):
#         self.cursor.execute(sql, params or ())
#         return self.fetchall()