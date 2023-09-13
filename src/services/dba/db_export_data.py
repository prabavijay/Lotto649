"""
    DBExportData - export data from tables
"""
from sqlalchemy.sql import func
import csv

FILE_ROOT_DIR = "/home/praba/my_github/keno_2023/"
DATA_LOCATION = FILE_ROOT_DIR + "data/"
EXPORTED_DRAWS_FILE = "exported_draws.csv"


class DBExportData:

    def __init__(self, db_connect, table_name):
        self.table_name = table_name
        self.db_connect = db_connect
        self.data_to_export = None

    def export_data_from_table(self):
        if self.table_name == "draw_results":
            self.get_all_data_from_draw_results()
            self.write_draw_results_to_csv_file()
        else:
            print("Not implemented yet for other tables!")
            # TODO: Exporting others tables (predictions_history, etc)

    # get all records from table draw_results
    def get_all_data_from_draw_results(self):
        DrawInfo = self.db_connect.base.classes.draw_results

        # get last records
        result = self.db_connect.session.query(DrawInfo).order_by(DrawInfo.id.asc())
        # self.latest_draw_id_in_db = result.id
        self.data_to_export = result

    def write_draw_results_to_csv_file(self):
        csv_file_name = DATA_LOCATION + EXPORTED_DRAWS_FILE
        fields = ["id", "draw_date", "draw_time",
                  "ball_1", "ball_2", "ball_3", "ball_4", "ball_5",
                  "ball_6", "ball_7", "ball_8", "ball_9", "ball_10",
                  "ball_11", "ball_12", "ball_13", "ball_14", "ball_15",
                  "ball_16", "ball_17", "ball_18", "ball_19", "ball_20"]

        with open(csv_file_name, 'w', newline='') as csv_file:
            csvwriter = csv.writer(csv_file, delimiter=',')
            csvwriter.writerow(fields)
            for draw in self.data_to_export:
                csvwriter.writerow([draw.id, draw.draw_date, draw.draw_time,
                                    draw.ball_1, draw.ball_2, draw.ball_3, draw.ball_4, draw.ball_5,
                                    draw.ball_6, draw.ball_7, draw.ball_8, draw.ball_9, draw.ball_10,
                                    draw.ball_11, draw.ball_12, draw.ball_13, draw.ball_14, draw.ball_15,
                                    draw.ball_16, draw.ball_17, draw.ball_18, draw.ball_19, draw.ball_20
                                    ])
