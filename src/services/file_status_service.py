"""
FileStatusService - service class to handle checking status of 'latest results from web' etc.
"""
import src.utils as utils
from datetime import datetime
from datetime import date, timedelta

import configparser

HOME_DIR = utils.get_home_dir()
FILE_ROOT_DIR = HOME_DIR + "/my_github/lotto649/"  # db/import_data/bulk_data_from_1996_to_2022.csv
DATA_LOCATION = FILE_ROOT_DIR + "db/import_data/"
OUTPUT_LOCATION = FILE_ROOT_DIR + "output/"


class FileStatusService:

    def __init__(self, expected_draw_date, db_last_draw_date):
        # print("in 1 - FileStatusService")
        config = configparser.ConfigParser()
        config.read(FILE_ROOT_DIR + "src/settings.ini")
        print(config['project']['DATA_LOCATION'])

        self.latest_draw_id = 0
        self.latest_draw_results = {}
        self.expected_draw_date = expected_draw_date
        self.last_draw_date_in_db = db_last_draw_date
        self.file_to_import = None
        self.is_file_up_to_date = False
        self.total_draws_expected = 0

    # entry point into FileStatusService
    def get_file_status(self):
        self.check_if_file_up_to_date()
        # output info to user
        file_status_note = f"need to update {self.file_to_import} with results from web"  # default
        while not self.is_file_up_to_date:
            print("File Status:", file_status_note.capitalize())
            print("PLEASE UPDATE THE FILE NOW!")
            # once, file is updated
            # Wait for the user input to continue or terminate the loop
            ans = input("Check file again? (y/n)")
            # Terminate the script if the input value is 'n'
            if ans.lower() == 'n':
                task = 'QUIT'
                break
            elif ans.lower() == 'y':
                self.check_if_file_up_to_date()
        if self.is_file_up_to_date:
            file_status_note_negative = "no " + file_status_note
            print("File Status:", file_status_note_negative.capitalize())
            print("You may proceed with DB update (to import results from the file)")

    # determines expected draw date & time as of current time & date
    # def get_expected_draw_date(self):
    #     self.expected_draw_date = utils.get_expected_draw_date()

    # assign location of file with up-to-date draw results
    def get_file_to_import(self, file_name):
        self.file_to_import = DATA_LOCATION + file_name

    # get status of the file  - whether it has up-to-date results as expected date & time
    def check_if_file_up_to_date(self):
        # --- EXPECTED FORMAT
        """
           9th September 2023	8	17	20	26	42	44	3
           6th September 2023	3	10	31	38	39	41	34
        """

        # get file that supposed to be with 'latest draw results' from web
        self.get_file_to_import("latest_649_from_web.csv")

        data = []
        with open(self.file_to_import, 'r') as f:
            for line in f:
                data_line = line.rstrip().split('\t')
                data.append(data_line)

        # read in all contents of the file
        # for date_line in data:
        #     if date_line[0].startswith("Daily Keno"):
        #         print(f"Your file {self.file_to_import}.csv has following dates: ", date_line[0])

        draw_num = 0
        all_dates_in_file = []
        draw_date_in_file = None
        print(f"Your file {self.file_to_import}.csv has following dates: ")
        for row in data:  # ['9th September 2023', '8', '17', '20', '26', '42', '44', '3']
            print(row)
            draw_num += 1
            draw_results = []
            draw_date_str = row[0].split(' ')
            date_part = draw_date_str[0][:-2]
            month = draw_date_str[1]
            year = draw_date_str[2]
            # print(date_part, month, year)
            draw_date_in_file = utils.string_to_date(date_part + "-" + month + "-" + year)
            # print(draw_date_in_file)
            all_dates_in_file.append(draw_date_in_file)

        self.calculate_number_of_draws_expected()
        print("Actual Date in File: ", all_dates_in_file[0])
        print("Expected Date in File: ", self.expected_draw_date)
        if utils.is_date2_latest(self.expected_draw_date, all_dates_in_file[0]):
            print("[INFO] File is up to date!")
            self.is_file_up_to_date = True
        else:
            print("[WARNING] File need to be updated BEFORE DB update!")
            self.is_file_up_to_date = False

    def calculate_number_of_draws_expected(self):
        # self.expected_draw_date = utils.get_expected_draw_date()
        # -- start_date = date(2023, 8, 4)
        db_draw_date = self.last_draw_date_in_db

        delta = self.expected_draw_date - db_draw_date
        self.total_draws_expected = delta.days

        print("Days Since: ", delta.days)
        print("Expected Total Draws: ", self.total_draws_expected)

