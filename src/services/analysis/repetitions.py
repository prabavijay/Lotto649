"""
Analyze 'Repetitions' related models
"""
from src.services.dba.db_queries import BasicQueries
import src.utils as utils
import src.services.basic_stats.repeated_frequent_missing_queries as rep_freq_miss_queries

class Repetitions:
    def __init__(self, db_connect):
        print("in Repetitions Analysis")
        self.db_connect = db_connect

        self.basic_queries = BasicQueries(self.db_connect)

        # get last draw information
        self.last_draw_id = self.basic_queries.last_draw_id
        (self.last_draw_date, self.last_draw_numbers) = self.get_last_draw_info(self.last_draw_id)
        self.last_draw_info = [self.last_draw_id, self.last_draw_date, self.last_draw_numbers]
        Repetitions.print_info("Last Draw:", self.last_draw_info)

        next_draw_timestamp = Repetitions.get_future_draw_info()
        # self.next_draw_date = next_draw_timestamp[0]
        self.next_draw_month = next_draw_timestamp[1]
        self.next_draw_dateofmonth = next_draw_timestamp[2]
        self.next_draw_day = next_draw_timestamp[3]
        self.future_draw_info = [self.next_draw_month, self.next_draw_dateofmonth, self.next_draw_day]
        Repetitions.print_info("Future Draw:", self.future_draw_info)

        # variables to hold individual stats
        self.repetition_stats = self.get_repetition_stats_from_db(self.last_draw_id)
        Repetitions.print_info("Repetition Stats:", self.repetition_stats)

    # TODO: get most common numbers repeated
    # TODO: get most common balls repeated
    # TODO: get associated numbers repeated together
    # TODO: get associated balls repeated together
    # TODO: when total_repeats >= n, what are the most common repeated numbers, balls, date-month-day
    # TODO: when total_repeats >= n, what are the subsequent numbers
    def get_last_draw_info(self, draw_id):
        return self.basic_queries.get_draw_date_numbers_by_id(draw_id)

    @staticmethod
    def get_future_draw_info():
        return utils.get_future_draw_date()

    @staticmethod
    def print_info(title, contents):
        print(f"------- {title}:")
        print(contents)

    def get_repetition_stats_from_db(self, draw_id):
        repetition_stats = {'Winning JackPot': True}
        # 1) get last row from the repetition table
        repetition_data_id = draw_id - 1
        repetition_data = self.basic_queries.get_data_from_stats_table('repetition', repetition_data_id)
        repetition_stats['total_repetitions'] = repetition_data[4]
        repetition_stats['repeated_nums'] = repetition_data[2]
        repetition_stats['repeated_balls'] = repetition_data[3]
        # 2) if total_repetitions < 4 then, set is_odds_to_repeat_high = True

        # 4) return dict of [is_odds_to_repeat_high, total_repeated, repeated_nums, repeated_balls]
        return repetition_stats