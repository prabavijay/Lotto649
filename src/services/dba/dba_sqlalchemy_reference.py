from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2
from psycopg2 import connect, Error
from getpass import getpass

create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks(
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    start_date DATE,
    due_date DATE,
    release_year YEAR(4),
    status TINYINT NOT NULL,
    priority TINYINT NOT NULL,
    description TEXT,
    rating DECIMAL(2,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

#--- create table with foreign key
create_checklists_table = """
CREATE TABLE IF NOT EXISTS checklists (
    todo_id INT AUTO_INCREMENT,
    task_id INT,
    todo VARCHAR(255) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (todo_id , task_id),
    FOREIGN KEY (task_id)
        REFERENCES tasks (task_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);
"""

tasks = [('Ford Automation', 1, 2),
         ('Sellooros Panels', 1, 3),
         ('OKNow Project', 2, 3)]

query_where_and_order_by = """SELECT title, status, priority FROM tasks 
WHERE
    title = 'OKNow Project' AND 
    priority = 3
ORDER BY 
    status DESC, 
    title ASC;"""

#TODO: MySQL INNER JOIN clause
"""SELECT 
    m.member_id, 
    m.name member, 
    c.committee_id, 
    c.name committee
FROM
    members m
INNER JOIN committees c 
	ON c.name = m.name;"""

class DBA_SQLAlchemy:

    def __init__(self):
        self.engine = self.create_engine()

    def create_engine(self):
        """Create database connection."""
        engine = create_engine(
                    "postgresql+psycopg2://kenouser:oknow2023@localhost/kenodb", echo=False
        )
        return engine

    def run_sql(self, sql_statement):
        conn = None

        try:
            conn = self.engine.connect()
            conn.execute(text(sql_statement))
        except Error as e:
            print(e)
        finally:
            conn.close()

    def run_query(self, sql_statement):
        "SELECT job_id, agency, business_title, \
                        salary_range_from, salary_range_to \
                        FROM nyc_jobs ORDER BY RAND();"
        conn = None
        result = None

        try:
            conn = self.engine.connect()
            result = conn.execute(text(sql_statement))
        except Error as e:
            print(e)
        finally:
            conn.close()
        return result

    def parse_result(self, query_result):
        print(f"Selected {query_result.rowcount} rows.")
        for row in query_result.fetchall():
            print(row['title'])

    def parse_result_into_dict(self, query_result):
        rows_dict = [dict(row) for row in query_result.fetchall()]
        return rows_dict

    #TODO:  Execute a SQsL query and fetch single row.
    def query_with_fetch_one(self, statement):
        result = self.run_query(statement).fetchone()
        print('Total Row(s):', len(result))
        return result

    #TODO:  Execute a SQsL query and fetch ALL rows.
    def query_with_fetch_all(self, statement):
        result = self.run_query(statement).fetchall()
        print('Total Row(s):', len(result))
        return result

    def iter_row(self, result_all, size=10):
        # generator to fetch 10 rows at a time
        while True:
            rows = result_all.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    #TODO:  Execute a SQsL query and fetch results by chunk.
    def query_with_fetch_many(self, statement, size=10):
        #  fetch N rows
        result_all = self.run_query(statement)
        result_chunk = self.iter_row(result_all, size)
        return result_chunk

    #TODO:  Create new DATABASE
    def create_database(self, dbname):
        create_db_sql = "CREATE DATABASE " + dbname
        self.run_sql(create_db_sql)

    #TODO: Create a table
    def create_table(self, statement):
        self.run_sql(statement)

    #TODO:  show all databases.
    def show_databases(self):
        databases = self.run_query("SHOW DATABASES").fetchall()
        for db in databases:
            print(db)

    # TODO: Show All tables
    def show_tables(self):
        tables = self.run_query("SHOW TABLES").fetchall()
        for table in tables:
            print(table)

    #TODO: Describe Table
    def describe_table(self, table):
        self.run_sql("DESCRIBE " + table + ";")

    #TODO: Get last row id
    def get_last_row_id(self, table='draw_results'):
        query_statement = "SELECT MAX(id) FROM  " + table + ";"
        last_id = self.run_query(query_statement).fetchone()[0]
        return last_id

    #TODO: Get list of row IDs
    def get_list_of_row_ids(self, table='draw_results'):
        query_statement = "SELECT id FROM  " + table + ";"
        id_list = self.run_query(query_statement).fetchall()
        return id_list

    #TODO: get list of IDs for n_rows
    def get_result_list(self, table, from_id, limit):
        # "SELECT * FROM foo WHERE id > 4 ORDER BY id LIMIT 1;"
        columns = "pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9, pos_10, \
        pos_11, pos_12, pos_13, pos_14, pos_15, pos_16, pos_17, pos_18, pos_19, pos_20"
        sql_statement = "SELECT  " + columns + " FROM " + table + " WHERE id <= " + str(from_id) + " ORDER BY id DESC LIMIT " + str(limit)
        draw_results = self.run_query(sql_statement).fetchall()
        return draw_results

    #TODO: Drop Table
    def drop_table(self, table):
        self.run_sql("DROP TABLE IF EXISTS " + table + ";")

    #TODO: Drop multiple tables
    def drop_tables(self, tables_list):
        tables_list_with_comma = ''
        for table in tables_list:
            tables_list_with_comma += table + ", "
        tables_list_with_comma = tables_list_with_comma[0:-2] # removing comma after last table
        self.run_sql("DROP TABLE " + tables_list_with_comma + ";")

    #TODO: truncate (Delete all rows) Table
    def truncate_tables(self, tables):
        for table in tables:
            self.run_sql("TRUNCATE TABLE " + table + ";")

    #TODO: Insert single row
    def insert_single_task(self, title, status, priority):
        args = "'" + title + "'" + "," + str(status) + "," + str(priority) + ")"
        sql_statement = "INSERT INTO tasks(title, status, priority) " \
                "VALUES(" + args

        self.run_sql(sql_statement)

    #TODO: Insert multiple rows into a table
    def insert_tasks(self,  title, status, priority):
        args = "'" + title + "'" + "," + str(status) + "," + str(priority) + ")"
        query = "INSERT INTO tasks(title, status, priority) " \
                "VALUES(" + args

        conn = None
        try:
            conn = self.engine.connect()
            conn.executemany(text(query))
        except Error as error:
            print(error)
        finally:
            conn.close()

    #TODO: UPDATE rows
    def update_task(self, title, task_id):
        sql_statement = """ UPDATE tasks
                SET title = 'PR'
                WHERE task_id = 6 """

        self.run_sql(sql_statement)

    #TODO: Delete specific row
    def delete_task(self, task_id):
        sql_statement = "DELETE FROM tasks WHERE task_id = " + str(task_id)

        self.run_sql(sql_statement)

    #TODO: Find duplicates in table regardless of unique ID.
    def find_duplicate_in_tasks(self):
        sql_find_duplicates = "SELECT task_id FROM tasks WHERE task_id NOT IN (SELECT min(task_id) " \
                              "FROM tasks GROUP BY title, status, priority);"
        return self.run_query(sql_find_duplicates)

    def find_duplicate_in_draw_results(self):
        # cur = self.conn.cursor()
        sql_find_duplicates = "SELECT id FROM draw_results WHERE id NOT IN (SELECT min(id) " \
                              "FROM draw_results GROUP BY draw_date,draw_time);"
        # cur.execute(sql_find_duplicates)
        with self.engine.connect() as conn:
            rows = conn.execute(text(sql_find_duplicates))
        return rows

    def find_duplicate_in_draw_results(self):
        # cur = self.conn.cursor()
        sql_find_duplicates = "SELECT id FROM draw_results WHERE id NOT IN (SELECT min(id) " \
                              "FROM draw_results GROUP BY pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, " \
                              "pos_7, pos_8, pos_9, pos_10, pos_11, pos_12, pos_13, pos_14, pos_15, pos_16, pos_17, " \
                              "pos_18, pos_19, pos_20);"
        with self.engine.connect() as conn:
            rows = conn.execute(text(sql_find_duplicates))
        return rows

    @staticmethod
    def test_database_api():
        #TODO:  TESTs for PostgreSQL server.

        dba_ops = DBA_SQLAlchemy()

        dba_ops.show_databases()

        dba_ops.create_table(create_tasks_table)
        dba_ops.show_tables()
        dba_ops.describe_table('tasks')


        dba_ops.create_table(create_checklists_table)
        dba_ops.show_tables()
        dba_ops.drop_table('checklists')
        # # mysql_ops.drop_tables(['checklists', 'tasks'])
        dba_ops.show_tables()

        dba_ops.insert_single_task('HELLO Learn Postgres INSERT Statement', 2, 1)
        dba_ops.delete_task(5)
        result = dba_ops.query_with_fetch_all("SELECT * FROM tasks")
        for row in result:
            print(row)

        print(dba_ops.get_last_row_id('tasks'))

        result = dba_ops.run_query("SELECT * FROM tasks")
        # dba.parse_result(result)
        result_dict = dba_ops.parse_result_into_dict(result)
        print(result_dict[1])

        result = dba_ops.find_duplicate_in_draw_results()
        result_dict = dba_ops.parse_result_into_dict(result)
        print(result_dict)

        dba_ops.update_task("Pyhton39", 6)
        print(dba_ops.get_last_row_id('tasks'))
#-------------------------------------------------
#TODO: MAIN TEST_CASES
# dba = DBA_SQLAlchemy()
# dba.test_mysql_api()



