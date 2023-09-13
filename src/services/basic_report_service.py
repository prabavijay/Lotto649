"""
BasicReportService - service class to handle composing Basic Report.
"""
from src.services.dba.db_queries import BasicQueries
import src.utils as utils
import src.services.basic_stats.repeated_frequent_missing_queries as rep_freq_miss_queries

class BasicReportService:
    def __init__(self, db_connect):
        print("in 5 - BasicReportService")
        self.db_connect = db_connect
        # get last draw information
        self.basic_queries = BasicQueries(self.db_connect)
        self.last_draw_id = self.basic_queries.last_draw_id
        (self.last_draw_date, self.last_draw_numbers) = (
            self.basic_queries.get_draw_date_numbers_by_id(self.last_draw_id))
        date_str = utils.date_to_string(self.last_draw_date)
        print(f"Following Stats are for: {date_str}")
        print("-----------")
        next_draw_timestamp = utils.get_future_draw_date()
        # self.next_draw_date = next_draw_timestamp[0]
        self.next_draw_month = next_draw_timestamp[1]
        self.next_draw_dateofmonth = next_draw_timestamp[2]
        self.next_draw_day = next_draw_timestamp[3]

        # variables to hold individual stats
        self.limit_for_ball = rep_freq_miss_queries.limit_for_ball
        self.limit_for_subseq = rep_freq_miss_queries.limit_for_subsequence
        self.repetition_stats = None
        self.freq_and_missn_stats = None
        self.subsequence_stats = None
        # freq_by_* stats
        self.pool_size_general = 10
        self.freq_by_date_stats = None
        self.freq_by_ball_stats = None
        self.freq_by_month_stats = None
        self.freq_by_day_stats = None

        self.collected_stats = self.collect_all_stats()

    def collect_all_stats(self):
        stats = {'repetition_stats': self.repetition_stats,
                 'freq_and_missn_stats': self.freq_and_missn_stats,
                 'subsequence_stats': self.subsequence_stats,
                 'freq_by_date_stats': self.freq_by_date_stats,
                 'freq_by_ball_stats': self.freq_by_ball_stats,
                 'freq_by_month_stats': self.freq_by_month_stats,
                 'freq_by_day_stats': self.freq_by_day_stats}
        return stats

    def process_all_stats(self):
        self.process_repetition_stats()
        self.process_freq_and_missn_stats()
        self.process_subsequence_stats()
        self.process_freq_by_date_stats()
        self.process_freq_by_ball_stats()
        self.process_freq_by_month_stats()
        self.process_freq_by_day_stats()
        return self.collect_all_stats()

    def process_repetition_stats(self):
        print("***** BasicReport: Processing repetition stats ...")
        self.repetition_stats = self.get_repetition_stats_from_db()
        BasicReportService.print_stats(self.repetition_stats, 'repetition')

    def get_repetition_stats_from_db(self):
        repetition_stats = {'Winning JackPot': True}
        # 1) get last row from the repetition table
        repetition_data_id = self.last_draw_id - 1
        repetition_data = self.basic_queries.get_data_from_stats_table('repetition', repetition_data_id)
        repetition_stats['total_repetitions'] = repetition_data[4]
        repetition_stats['repeated_nums'] = repetition_data[2]
        repetition_stats['repeated_balls'] = repetition_data[3]
        # 2) if total_repetitions < 4 then, set is_odds_to_repeat_high = True

        # 4) return dict of [is_odds_to_repeat_high, total_repeated, repeated_nums, repeated_balls]
        return repetition_stats

    def process_freq_and_missn_stats(self):
        print("***** BasicReport: Processing frequented_and_missing_stats stats ...")
        self.freq_and_missn_stats = self.get_freq_and_missn_stats_from_db()
        BasicReportService.print_stats(self.freq_and_missn_stats, 'freq_and_missn')

    def get_freq_and_missn_stats_from_db(self):
        freq_and_missn_stats = {}
        freq_and_missn_data = self.basic_queries.get_data_from_stats_table(
            'freq_and_missn', self.last_draw_id)
        freq_and_missn_stats['freq_and_missing'] = freq_and_missn_data[4]
        freq_and_missn_stats['frequented_nums'] = freq_and_missn_data[2]
        freq_and_missn_stats['missing_nums'] = freq_and_missn_data[3]

        return freq_and_missn_stats

    def process_subsequence_stats(self):
        print("***** BasicReport: Processing subsequence stats ...")
        self.subsequence_stats = self.get_subsequence_stats_from_db()
        BasicReportService.print_stats_nested_dict(self.subsequence_stats)
        # print(self.subsequence_stats)

    def get_subsequence_stats_from_db(self):
        subsequence_stats = {}
        last_drawn_numbers = self.last_draw_numbers
        print(f"Last Drawn Numbers: {last_drawn_numbers}")
        ball_number = 1
        pool_size = self.limit_for_subseq
        for base_number in last_drawn_numbers:

            subsequence_numbers = self.basic_queries.get_most_frequented_subsequence_numbes(ball_number, base_number, pool_size)
            list_of_subseq_numbers_dict = []

            for item in subsequence_numbers:
                subseq_dict = {
                    'subseq_num': item[0],
                    'freq': item[1]
                }
                list_of_subseq_numbers_dict.append(subseq_dict)
            key_ball_number = f'ball_num_{ball_number}'
            subsequence_stats[key_ball_number] = list_of_subseq_numbers_dict
            # print(subsequence_stats[ball_number])
            ball_number += 1

        return subsequence_stats

    def process_freq_by_date_stats(self):
        # # date_3 (freq_by_date)
        # # select drawn_number, date_3 from freq_by_date order by date_3 desc limit 10;
        print("***** BasicReport: Processing freq_by_date stats ...")
        self.freq_by_date_stats = self.get_freq_by_date_stats_from_db()
        BasicReportService.print_stats(self.freq_by_date_stats, 'date')

    def get_freq_by_date_stats_from_db(self):
        freq_by_date_stats = {}
        filter_by = f"date_{self.next_draw_dateofmonth}"
        pool_size = self.pool_size_general
        freq_by_date_data = self.basic_queries.get_data_from_freq_by_table('freq_by_date', filter_by, pool_size)
        for item in freq_by_date_data:
            freq_by_date_stats[item[0]] = item[1]
        return freq_by_date_stats

    def process_freq_by_month_stats(self):
        # # month = sep
        # select drawn_number, sep from freq_by_month order by sep desc limit 10;
        print("***** BasicReport: Processing freq_by_month stats ...")
        self.freq_by_month_stats = self.get_freq_by_month_stats_from_db()
        BasicReportService.print_stats(self.freq_by_month_stats, 'month')

    def get_freq_by_month_stats_from_db(self):
        freq_by_month_stats = {}
        filter_by = self.next_draw_month
        pool_size = self.pool_size_general
        freq_by_month_data = self.basic_queries.get_data_from_freq_by_table('freq_by_month', filter_by, pool_size)
        for item in freq_by_month_data:
            freq_by_month_stats[item[0]] = item[1]
        return freq_by_month_stats

    def process_freq_by_day_stats(self):
        # # day = sun
        # select drawn_number, sun from freq_by_day order by sun desc limit 10;
        print("***** BasicReport: Processing freq_by_day stats ...")
        self.freq_by_day_stats = self.get_freq_by_day_stats_from_db()
        BasicReportService.print_stats(self.freq_by_day_stats, 'day')

    def get_freq_by_day_stats_from_db(self):
        freq_by_day_stats = {}
        filter_by = self.next_draw_day
        pool_size = self.pool_size_general
        freq_by_day_data = self.basic_queries.get_data_from_freq_by_table('freq_by_day', filter_by, pool_size)
        for item in freq_by_day_data:
            freq_by_day_stats[item[0]] = item[1]
        return freq_by_day_stats

    def process_freq_by_ball_stats(self):
        # # ball_1..20 (freq_by_ball)
        # select drawn_number, ball_1 from freq_by_ball order by ball_1 desc limit 10;
        # select drawn_number, ball_20 from freq_by_ball order by ball_20 desc limit 10;
        print("***** BasicReport: Processing freq_by_ball stats ...")
        self.freq_by_ball_stats = self.get_freq_by_ball_stats_from_db()
        BasicReportService.print_stats(self.freq_by_ball_stats, 'ball')

    def get_freq_by_ball_stats_from_db(self):
        freq_by_ball_stats = {}

        pool_size = self.limit_for_ball
        for ball in range(1, 8):
            filter_by = f"ball_{ball}"
            freq_by_ball_data = self.basic_queries.get_data_from_freq_by_table('freq_by_ball', filter_by, pool_size)
            list_of_ball_dict = []
            for item in freq_by_ball_data:
                ball_dict = {
                    'drawn_num': item[0],
                    'freq': item[1]
                }
                list_of_ball_dict.append(ball_dict)
            freq_by_ball_stats[filter_by] = list_of_ball_dict

        return freq_by_ball_stats

    @staticmethod
    def print_stats(stats, stats_type):
        if stats_type in ['date', 'month', 'day', 'time']:
            print(list(stats.keys()))
        else:
            for key, value in stats.items():
                if isinstance(value, str) and value.startswith('{'):
                    value = utils.convert_string_to_list_of_numbers(value)
                if isinstance(key, str) and key.startswith('ball_'):
                    ball_freq_dict = value[0]
                    value = ball_freq_dict['drawn_num']
                print(key, ": ", value)

    @staticmethod
    def print_stats_nested_dict(stats):
        num_by_ball = []
        for ball, num_list in stats.items():
            sublist = []
            for num_dict in num_list:
                for key, value in num_dict.items():
                    if key == 'drawn_num' or key == 'subseq_num':
                        # print(ball, ": ", value)
                        sublist.append(value)
            num_by_ball.append(sublist)
        print(num_by_ball)