"""
ImportDataService - service class to handle importing data (both latest_draw_results & archived).
"""
import platform
import csv
import operator
# import os.path
from sqlalchemy import func, text, delete
from datetime import datetime
from src.utils import sql_result_to_list, get_home_dir, string_to_date
from src.services.dba.db_model import DrawResults
from datetime import datetime, timedelta


HOME_DIR = get_home_dir()
FILE_ROOT_DIR = HOME_DIR + "/my_github/lotto649/"
DATA_LOCATION = FILE_ROOT_DIR + "db/import_data/"
BULK_DRAWS_FILE = "l649_results_1982_2023.csv"
LATEST_DRAWS_FILE = "latest_649_from_web.csv"
OUTPUT_LOCATION = FILE_ROOT_DIR + "output/"


class ImportDataService:

    def __init__(self, db_connect, import_type='latest_draws'):
        print("in 3 - ImportDataService")
        self.db_connect = db_connect
        self.import_type = import_type
        self.file_to_import = self.get_data_file()
        self.data_to_insert = None

    def get_data_file(self):
        data_file = None
        if self.import_type == 'bulk_draws':
            data_file = DATA_LOCATION + BULK_DRAWS_FILE
        elif self.import_type == 'latest_draws':
            data_file = DATA_LOCATION + LATEST_DRAWS_FILE
        return data_file

    def import_data_into_db(self):
        if self.import_type == 'bulk_draws':
            self.data_to_insert = self.extract_bulk_draws_from_file()
            self.insert_bulk_draws_into_db()
        elif self.import_type == 'latest_draws':
            self.data_to_insert = self.extract_latest_draws_from_file()
            self.insert_latest_draws_into_db()

    def extract_latest_draws_from_file(self):
        # --- Expected format for data in 'latest draw results' file
        """
           Daily Keno Dec 29 2021 (2021-12-29 Wed) E
        1	4	9	20	21	23	29	31	33	34
        39	41	45	46	49	53	54	59	62	65
           ENCORE: 3749655    Encore Payout 2021-12-29

           Daily Keno Dec 29 2021 (2021-12-29 Wed) M
        6	7	8	9	10	11	15	18	25	26
        34	41	43	45	51	54	55	59	67	68
           ENCORE: 6496799    Encore Payout 2021-12-29
        """

        # calculate total number of draws in file
        lines_count = 1
        with open(self.file_to_import, 'r') as latest_draws_file:
            for line in latest_draws_file:
                lines_count = lines_count + 1
        # each draw info takes up 5 lines
        total_draws = lines_count//5
        print(f"Total number of Draws found in data file: {total_draws}")
        # print(f"WARNING: will process last {total_draws} draws only!")

        # --- Start parsing data
        try:
            with open(self.file_to_import, 'r') as latest_draws_file:
                reader = csv.reader(latest_draws_file, delimiter='\t')
                data_to_import = []
                draw_result = []
                drawn_numbers = []
                # print("LINE: ", reader[0])
                draw_num = 0
                for row in reader:
                    if len(row) != 0:
                        row_string = row[0].strip()

                    draw_date = ""
                    draw_time = ""
                    # --- Process Draw Date + Time Info
                    if row_string.startswith("Daily"):
                        string_to_parse = row_string.split('(')[1].split(')')
                        full_date = string_to_parse[0].split(" ")[0]
                        draw_time_char = string_to_parse[1].split("'")[0].strip()
                        if draw_time_char == 'M':
                            draw_time = '14:00:00'
                        elif draw_time_char == 'E':
                            draw_time = '23:00:00'
                        draw_num += 1
                        draw_result = [full_date, draw_time]
                        drawn_numbers = []

                    # -- Process  Num1 to Num 20
                    elif not row_string.startswith("Daily") and not row_string.startswith("ENCORE") and row_string != '' :
                        # drawn_numbers = row.split('	')
                        drawn_numbers.extend(row)
                    elif len(drawn_numbers) == 20:
                        draw_result.extend(drawn_numbers)
                        drawn_numbers = []
                        data_to_import.append(draw_result)

            draw_data_with_date = []
            sorted_list = []
            for item in data_to_import:
                item_to_insert = []
                item_to_insert.extend(item)
                draw_data_with_date.append(item_to_insert)
                # sort by date(asc), time (asc)
                sorted_list = sorted(draw_data_with_date, key = operator.itemgetter(0,1) )
            for record in sorted_list:
                print(record)
            return sorted_list
        except IOError as e:
            print("ERROR: opening CSV")

    @staticmethod
    def string_to_date(str_date):
        # '9th September 2023'
        datetime_obj = datetime.strptime(str_date, '%d %M %Y')
        return datetime_obj.date()

    def extract_bulk_draws_from_file(self):
        # --- Expected format for data in 'bulk draws' file
        """
        1,1996-04-29,23:00:00,1,2,4,6,9,13,15,16,21,28,34,37,41,48,50,52,53,54,57,68
        2,1996-04-30,23:00:00,6,7,10,17,23,24,27,28,31,39,42,43,46,48,50,55,60,61,67,70
        ...
        14002,2023-07-18,14:00:00,3,4,7,8,15,19,23,27,29,30,33,41,46,47,49,50,60,61,63,64
        14003,2023-07-18,23:00:00,3,5,9,11,23,25,38,39,44,45,46,47,52,55,56,57,63,64,66,70
        """

        lines_count = 0
        with open(self.file_to_import, 'r') as bulk_data_file:
            for line in bulk_data_file:
                lines_count = lines_count + 1
        print(f"Total number of lines : {lines_count}")
        print(f"Total number of Draws found in data: {lines_count}")
        # print(f"WARNING: will process last {total_draws} draws only!")

        # --- Start parsing data
        try:
            with open(self.file_to_import, 'r') as bulk_data_file:
                reader = csv.reader(bulk_data_file, delimiter='\t')
                data_to_import = []
                draw_results = []
                # print("LINE: ", reader[0])
                draw_num = 0

                for row in reader: # ['9th September 2023', '8', '17', '20', '26', '42', '44', '3']
                    print(f"INPUT: {row}")
                    draw_num += 1
                    draw_results = []
                    draw_date_str = row[0].split(' ')
                    date_part = draw_date_str[0][:-2]
                    month = draw_date_str[1]
                    year = draw_date_str[2]
                    # print(date_part, month, year)
                    draw_date = string_to_date(date_part + "-" + month + "-" + year)
                    # print(draw_date)
                    result_list_str = row[1:]
                    result = []
                    for str in result_list_str:
                        result.append(int(str))
                    draw_results.append(draw_date)
                    draw_results.append(result)
                    data_to_import.append(draw_results)
                    print(f"DATA TO INSERT: {draw_results}")

                data_to_import.reverse() # reverse the list so the oldest is the first
                print(f"Total number of lines : {lines_count}")
                print(f"Total number of Draws found in data: {lines_count}")
                print(f"First Record : {data_to_import[0][0]} : {data_to_import[0][1]}")
                print(f"Last Record : {data_to_import[-1][0]} : {data_to_import[-1][1]}")
                return data_to_import
        except IOError as e:
            print("ERROR: opening CSV")

    def insert_bulk_draws_into_db(self):

        if self.data_to_insert is not None:
            # latest_id = int(self.get_last_row_id())
            print("[INFO] Inserting Bulk of draw results from CSV into DB ...")

            for row in self.data_to_insert:
                info_date = row[0]
                info_result = row[1]
                draw_info_to_insert = DrawResults(info_date, info_result)
                self.db_connect.session.add(draw_info_to_insert)

                # commit and close session
            self.db_connect.session.commit()
        else:
            print("[ERROR] Extracting data from CSV Failed!")

    def insert_latest_draws_into_db(self):
        if self.data_to_insert is not None:
            for row in self.data_to_insert:
                draw_date = row[0]
                draw_time = row[1]

                draw_result = row[2:]
                draw_result_to_insert = DrawResults(draw_date, draw_time, draw_result)
                with self.db_connect.engine.connect() as conn:
                    transaction = conn.begin()
                    self.db_connect.session.add(draw_result_to_insert)
                    transaction.commit()

                # commit and close session
            self.db_connect.session.commit()

    def delete_duplicates(self):
        # -- delete duplicates from Draw_Info table
        self.find_duplicate_in_draw_results()
        self.delete_duplicates_in_draw_results()

    def find_duplicate_in_draw_results(self):
        results = None
        # -- to make it fast query, we're assuming bulk data doesn't have duplicates,
        # so we're searching where id > 14000
        sql_find_duplicates = text("SELECT id from draw_results dr where (select count(*) from draw_results dr2"
                                   " where dr.id > 14000"
                                   " and dr.draw_date = dr2.draw_date"
                                   " and dr.draw_time = dr2.draw_time ) > 1")

        with self.db_connect.engine.connect() as conn:
            results = conn.execute(sql_find_duplicates)

        id_list = sql_result_to_list(results)
        if len(id_list) != 0:
            print("Found following duplicates:")
            for row_id in id_list:
                print(row_id)

    def delete_duplicates_in_draw_results(self):
        sql_to_delete_duplicates = text("DELETE FROM draw_results dr1 USING draw_results dr2 "
                                        "where dr1.draw_date = dr2.draw_date "
                                        "AND dr1.draw_time = dr2.draw_time "
                                        "AND dr2.id > dr1.id")
        with self.db_connect.engine.connect() as conn:
            transaction = conn.begin()
            results = conn.execute(sql_to_delete_duplicates)
            transaction.commit()

    def delete_row_by_id_sqlalchemy(self, table, id_column_name, ids):
        # cur = self.conn.cursor()
        for row_id in ids:
            statement = delete(DrawResults).where(DrawResults.id.in_(row_id))
            self.db_connect.session.execute(statement)
            self.db_connect.session.commit()
