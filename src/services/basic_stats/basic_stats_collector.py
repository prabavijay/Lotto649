"""
this class implements methods to do the following:
1. construct a dictionary to hold basic_stats
2. read each record/row from 'draw_results' table
3. on-hold: convert the record/row into a dictionary
4. (class BasicStatsUpdater) construct SQL statements to update various frequency-tracking '*stats' tables
5. (class BasicStatsUpdater) update frequency-tracking '*stats' tables
6. (class BasicStatsService) sanity-check frequency-tracking '*stats' tables Using 'group by' queries
"""
import src.utils as utils
from src.services.basic_stats.basic_stats_updater import BasicStatsUpdater
from src.services.basic_stats.frequent_by_queries import FrequentByQueries
from src.services.basic_stats.repeated_frequent_missing_queries import RepeatedFrequentMissingQueries
from src.services.basic_stats.subsequence_query import SubsequenceQuery
from src.services.dba.db_model import DrawResults


class BasicStatsCollector:
    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.freq_by_queries = FrequentByQueries(self.db_connect)
        self.basic_stats_dict = {}
        # ----------------------------------------------------------------
        self.freq_by_evening = None
        self.freq_by_midday = None
        self.freq_by_balls = None
        self.freq_by_months = None
        self.freq_by_days = None
        self.freq_by_dates = None
        self.stats_updater = BasicStatsUpdater(self.db_connect)
        # ----------------------------------------------------------------
        self.repeted_freq_missn_queries = RepeatedFrequentMissingQueries(self.db_connect)
        self.repetition_stats = None
        # ----------------------------------------------------------------
        self.frequented_numbers = None
        self.missing_numbers = None
        self.freq_but_missing_numbers = None
        self.freq_missn_stats = {}
        # ----------------------------------------------------------------
        self.subsequence_stats = None
        self.subsequence_query = SubsequenceQuery(self.db_connect)

    def get_draw_results_into_dict(self):
        # this method "SELECT * FROM draw_result", then create a dict of rows

        draw_info_all = self.db_connect.session.query(DrawResults).all()
        results_list = []
        for record in draw_info_all:
            results_list.append(utils.object_to_dict(record))

        return results_list

    def build_basic_stats(self, stats_to_skip):
        # Collect statistics and build a dictionary of basic stats

        # --- by Ball ---
        if 'freq_by_ball' not in stats_to_skip:
            print("***** Collecting Freq. by Balls ...")
            # # self.get_freq_by_specific_ball(1)
            self.freq_by_balls = self.freq_by_queries.get_freq_by_balls()
            self.basic_stats_dict['balls'] = self.freq_by_balls

        # --- by Month ---
        if 'freq_by_month' not in stats_to_skip:
            print("***** Collecting Freq. by Months ...")
            # # self.get_freq_by_specific_month(1)
            self.freq_by_months = self.freq_by_queries.get_freq_by_months()
            self.basic_stats_dict['months'] = self.freq_by_months

        # --- by Day ---
        if 'freq_by_day' not in stats_to_skip:
            print("***** Collecting Freq. by Days ...")
            # # self.get_freq_by_specific_day('mon')
            self.freq_by_days = self.freq_by_queries.get_freq_by_days()
            self.basic_stats_dict['days'] = self.freq_by_days

        # --- by Date ---
        if 'freq_by_date' not in stats_to_skip:
            print("***** Collecting Freq. by Dates ...")
            # # self.freq_by_queries.get_freq_by_specific_date_of_month(31)
            self.freq_by_dates = self.freq_by_queries.get_freq_by_dates_of_month()
            self.basic_stats_dict['dates'] = self.freq_by_dates

        return self.basic_stats_dict

    def build_repetition_stats(self):
        print("***** Collecting Repetition stats ...")
        self.repetition_stats = self.repeted_freq_missn_queries.get_bulk_repetition_stats()

    def build_freq_and_missing_stats(self):
        print("***** Collecting Freq. and Missing stats ...")
        self.freq_missn_stats['id'] = self.repeted_freq_missn_queries.last_draw_id
        self.freq_missn_stats['draw_date'] = self.repeted_freq_missn_queries.last_draw_date
        self.frequented_numbers = self.repeted_freq_missn_queries.get_frequented_numbers()
        self.freq_missn_stats['frequented'] = self.frequented_numbers
        self.missing_numbers = self.repeted_freq_missn_queries.get_missing_numbers()
        self.freq_missn_stats['missing'] = self.missing_numbers
        self.freq_but_missing_numbers = self.repeted_freq_missn_queries.get_freq_but_missing_numbers()
        self.freq_missn_stats['freq_but_missing'] = self.freq_but_missing_numbers
        self.freq_missn_stats['pool_size_freq'] = self.repeted_freq_missn_queries.pool_size_frequented
        self.freq_missn_stats['pool_size_missing'] = self.repeted_freq_missn_queries.pool_size_missing

        return self.freq_missn_stats

    def build_subsequence_stats(self):
        print("***** Collecting Subsequence stats ...")
        self.subsequence_stats = self.subsequence_query.get_subsequence_numbers()
        # print(self.subsequence_stats)
        # for key, value in self.subsequence_stats.items():
        #     print(key, value)

    def update_basic_stats(self, stats_to_skip):
        if 'freq_by_ball' not in stats_to_skip:
            self.stats_updater.update_freq_by_balls(self.freq_by_balls)
        if 'freq_by_month' not in stats_to_skip:
            self.stats_updater.update_freq_by_months(self.freq_by_months)
        if 'freq_by_day' not in stats_to_skip:
            self.stats_updater.update_freq_by_days(self.freq_by_days)
        if 'freq_by_date' not in stats_to_skip:
            self.stats_updater.update_freq_by_dates(self.freq_by_dates)

    def update_repetition_stats(self):
        # -- use bulk insert for large sets of insert
        self.stats_updater.update_repetition_stats(self.repetition_stats)
        # -- use update for regular(daily/weekly) updates
        # self.stats_updater.update_repetition_stats(self.repetition_stats)

    def update_freq_and_missing_stats(self):
        # use update for regular(daily/weekly) updates
        self.stats_updater.update_freq_and_missing_stats(self.freq_missn_stats)

    def update_subsequence_stats(self):
        # -- use bulk insert for large sets of insert
        self.stats_updater.bulk_insert_subsequence_numbers(self.subsequence_stats)
        # -- use update for regular(daily/weekly) updates
        self.stats_updater.update_subsequence_numbers(self.subsequence_stats)
# ========================
# {
#    "1":[
#       {
#          "times":{
#             "midday":0,
#             "evening":0
#          },
#          "days":{
#             "mon":0,
#             "tue":0,
#             "wed":0,
#             "thu":0,
#             "fri":0,
#             "sat":0,
#             "sun":0
#          },
#          "dates":{},
#          "months":{
#             "jan":0,
#             "feb":0,
#             "mar":0,
#             "apr":0,
#             "may":0,
#             "jun":0,
#             "jul":0,
#             "aug":0,
#             "sep":0,
#             "oct":0,
#             "nov":0,
#             "dec":0
#          },
#          "balls":{
#             "ball_1":0,
#             "ball_2":0,
#             "ball_3":0,
#             "ball_4":0,
#             "ball_5":0,
#             "ball_6":0,
#             "ball_7":0,
#             "ball_8":0,
#             "ball_9":0,
#             "ball_10":0,
#             "ball_11":0,
#             "ball_12":0,
#             "ball_13":0,
#             "ball_14":0,
#             "ball_15":0,
#             "ball_16":0,
#             "ball_17":0,
#             "ball_18":0,
#             "ball_19":0,
#             "ball_20":0
#          }
#       }
#    ],
