"""
1) If last draw repeated only 3 numbers from previous draw, then chance of repeating 8 numbers from last draw into next draw
2) In the last 20 draws, if a number has more than 7 frequency, but not drawn in last 5 draws, then chance is higher for that number
3) ADVANCED: If a number doesn’t skip more than 5 consecutive draws, based on last 20 draws, but not drawn in LAST 5-draws, then chance is higher for that number
"""

from src.services.dba.db_queries import BasicQueries
import random
import operator

freq20_but_miss5 = [20, 5]
pool_size_frequented = 20
freq_limit_freq_numbers = 5
pool_size_missing = 5
limit_for_subsequence = 3
limit_for_ball = 1


class RepeatedFrequentMissingQueries:
    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.basic_queries = BasicQueries(self.db_connect)
        self.last_draw_id = self.get_id_from_last_draw_results()
        self.last_draw_date, self.last_drawn_numbers = self.get_draw_date(self.last_draw_id)
        self.second_last_draw_id = self.get_id_from_second_last_draw_results()
        (self.number_of_repeats,
         self.numbers_repeated,
         self.balls_repeated) = self.get_repetition_stats()
        self.frequented = {}
        self.missing = None
        self.pool_size_frequented = pool_size_frequented
        self.freq_limit_freq_numbers = freq_limit_freq_numbers
        self.pool_size_missing = pool_size_missing
        self.freq_but_missing = None

    def get_id_from_last_draw_results(self):
        return self.basic_queries.last_draw_id

    def get_id_from_second_last_draw_results(self):
        return self.basic_queries.second_last_draw_id

    def get_last_draw_results(self):
        # get results for the id
        return self.basic_queries.get_last_draw_results()

    def get_second_last_draw_results(self):
        # get results for the id
        return self.basic_queries.get_second_last_draw_results()

    def get_draw_date(self, draw_id):
        return self.basic_queries.get_draw_date_numbers_by_id(draw_id)

    def get_repetition_stats(self):
        # -- to use in daily/weekly
        numbers_repeated, balls_repeated = self.find_repetitions(self.basic_queries.second_last_drawn_numbers,
                              self.basic_queries.last_drawn_numbers)

        number_of_repeats = len(numbers_repeated)
        return number_of_repeats, numbers_repeated, balls_repeated


    def get_bulk_repetition_stats(self):
        print("... Processing bulk repetition stats...")
        repetition_bulk_data = []
        # 1) get list of draws IDs
        row_ids = self.basic_queries.get_list_of_row_ids()
        last_draw_id = row_ids[-1]

        # 2) get draw numbers from base_draw
        for id in row_ids:
            numbers_repeated, balls_repeated = 0, 0
            base_draw_id = id
            if base_draw_id == last_draw_id:
                break
            id_index_in_ids = row_ids.index(base_draw_id)
            base_draw = self.basic_queries.get_draw_results_by_id(base_draw_id)

            # 3) get draw numbers from subseq_draw
            subseq_draw_id = row_ids[id_index_in_ids + 1]
            subseq_draw = self.basic_queries.get_draw_results_by_id(subseq_draw_id)
            # -- to use while analyzing all records in draw_results table
            numbers_repeated, balls_repeated = self.find_repetitions(base_draw, subseq_draw)
            number_of_repeats = len(numbers_repeated)
            draw_date, draw_numbers = self.get_draw_date(base_draw_id)

            row_data = [base_draw_id, draw_date, numbers_repeated, balls_repeated, number_of_repeats]
            repetition_bulk_data.append(row_data)
        return repetition_bulk_data

    def find_repetitions(self, from_base_draw, to_draw):
        # If last draw repeated only 3 numbers from previous draw, then chance of repeating 8 numbers from last draw into next draw

        # second_last_draw same as from_draw
        # last_draw same as to_draw
        numbers_repeated = []
        balls_repeated = []

        for base_index in range(0, 6):
            base_draw_item = from_base_draw[base_index]
            if from_base_draw[base_index] in to_draw:
                numbers_repeated.append(from_base_draw[base_index])
                position_in_base_draw = base_index + 1  # to non-zero based index
                balls_repeated.append(position_in_base_draw)
        return numbers_repeated, balls_repeated

    def get_frequented_numbers(self):
        # get draw results for last n row
        print("PROCESSING 'frequented_numbers'...")
        drawn_numbers_in_last_n_draws = self.basic_queries.get_n_draws_results(self.last_draw_id,
                                                                               self.pool_size_frequented)
        # for draw in drawn_numbers_in_last_n_draws:
        #     print(draw)
        frequented_sorted_by_key = RepeatedFrequentMissingQueries.frequented_numbers_last_n_draws(drawn_numbers_in_last_n_draws)
        sorted_by_value_desc_dict = sorted(frequented_sorted_by_key.items(), key=lambda x: x[1], reverse=True)
        converted_dict = dict(sorted_by_value_desc_dict)
        self.frequented = converted_dict
        return converted_dict

    @staticmethod
    def frequented_numbers_last_n_draws(n_draws_data):
        num_dict = {}
        for i in range(1, 50):
            num_dict[i] = 0
        for draw in n_draws_data:
            for number in draw[2:8]:
                key = int(number)
                num_dict[key] = num_dict[key] + 1

        sorted_d = sorted((value, key) for (key, value) in num_dict.items())
        # print(sorted_d)
        # top_10_by_frequency = sorted_d[int(-10):]
        # print("----")
        return num_dict

    def get_missing_numbers(self):
        print("PROCESSING 'missing_numbers'...")
        # get draw results for last n row
        drawn_numbers_in_last_n_draws = self.basic_queries.get_n_draws_results(self.last_draw_id,
                                                                               self.pool_size_missing)
        # for draw in drawn_numbers_in_last_n_draws:
        #     print(draw)
        missing_sorted_by_key = RepeatedFrequentMissingQueries.missing_numbers_last_n_draws(drawn_numbers_in_last_n_draws)
        self.missing = missing_sorted_by_key
        return self.missing

    @staticmethod
    def missing_numbers_last_n_draws(n_draws_data):
        missing_numbers_list = [num for num in range(1, 50)] # assume all 70 numbers are missing :-)
        for draw in n_draws_data:
            for num in draw[2:8]:
                if num in missing_numbers_list: # remove drawn number from list of missing
                    missing_numbers_list.remove(num)
        return sorted(missing_numbers_list)

    def get_freq_but_missing_numbers(self):
        # In the last 20 draws, if a number has more than 7 frequency, but not drawn in last 5 draws, then chance is higher for that number
        self.freq_but_missing = self.get_freq_n_but_miss_in_n_draws(self.pool_size_missing, self.freq_limit_freq_numbers)
        return self.freq_but_missing

    def get_freq_n_but_miss_in_n_draws(self, miss_limit=5, freq_pool_size=20, freq_limit=5):
        # --- Missing numbers in last 5 draws, BUT Frequency >= 8 in last 20 draws
        missing_numbers_in_n_draws = self.missing
        frequented_numbers_in_n_draws = self.frequented

        # print("FREQUENCY >= 8 in LAST_20_DRAWS AND MISSING IN LAST 5 DRAWS")
        freq_but_missing_numbers = []
        for number in missing_numbers_in_n_draws:
            if number in frequented_numbers_in_n_draws.keys():
                # print(number)
                if frequented_numbers_in_n_draws[number] >= freq_limit:
                    freq_but_missing_numbers.append(number)
            # else: # just list out frequency of missing numbers
            #     print(frequency_in_last_n_draws[int(number)])
        return freq_but_missing_numbers



