"""
DBStatusService - service class to handle checking status of DB etc.
"""

from src import utils


class DBStatusService:
    def __init__(self, db_connect, expected_draw_date):
        # print("in 2 - DBStatusService")
        self.conn = db_connect
        self.base = db_connect.base
        self.session = db_connect.session
        self.expected_draw_date = expected_draw_date
        self.last_draw_id_in_db = None
        self.last_draw_date_in_db = None
        self.is_db_up_to_date = False

    # find the last record of draw_results table; most likely latest within DB
    def get_latest_record_in_db(self, last_id):
        DrawResults = self.base.classes.draw_results

        # get last records
        result = self.session.query(DrawResults).filter(DrawResults.id == last_id)
        last_draw_record = None
        for item in result:
            last_draw_record = item
        self.last_draw_id_in_db = last_draw_record.id

        self.last_draw_date_in_db = last_draw_record.draw_date
        print("Last Record in DB: ", self.last_draw_id_in_db, self.last_draw_date_in_db)

    def get_db_status(self):
        if self.last_draw_date_in_db == self.expected_draw_date:
            print("[INFO] No update needed")
            self.is_db_up_to_date = True
        else:
            print("[WARNING] DB Need update")
            self.is_db_up_to_date = False
