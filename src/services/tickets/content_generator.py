import src.utils as utils
from src.services.tickets.wheels import Wheel
import src.services.basic_stats.repeated_frequent_missing_queries as rep_freq_miss_queries


collectn_size = None # 6 or 10
# thu evening
drawn_numbers = [8,17,20,26,42,44,3]
class Contents:

    def __init__(self, report_service, collected_stats, basic_stats_wheel):
        self.service = report_service
        self.drawn_numbers = drawn_numbers
        # self.drawn_numbers = self.service.last_draw_numbers
        self.repetitions_stats = collected_stats['repetition_stats']
        self.freq_and_missn_stats = collected_stats['freq_and_missn_stats']
        self.subsequence_stats = collected_stats['subsequence_stats']
        self.freq_by_date_stats = collected_stats['freq_by_date_stats']
        self.freq_by_ball_stats = collected_stats['freq_by_ball_stats']
        self.freq_by_month_stats = collected_stats['freq_by_month_stats']
        self.freq_by_day_stats = collected_stats['freq_by_day_stats']

        self.wheel = basic_stats_wheel

        self.today = utils.get_today_date(True)
        self.print_info_last_draw()
        self.print_info_next_draw()

        # ---------- Top Level Categories
        self.print_repetitions_stats()
        self.freq_numbers, self.missn_numbers = self.print_freq_and_missn_stats()
        self.subseq_numbers = self.print_subsequence_stats()

        # ---------- Frequented By Categories
        self.date_numbers = self.print_freq_by_date_stats()
        self.ball_numbers = self.print_freq_by_ball_stats()
        self.month_numbers = self.print_freq_by_month_stats()
        self.day_numbers = self.print_freq_by_day_stats()

        # ---------- Subsequence Combinations
        # TODO: subsequence and frequented
        self.subseq_n_freq = self.print_subseq_n_freq_numbers()
        # TODO: subsequence and missing
        self.subseq_n_missn = self.print_subseq_n_missn_numbers()
        # TODO: subsequence and date
        self.subseq_n_date = self.print_subseq_n_date_numbers()
        # TODO: subsequence and ball
        self.subseq_n_ball = self.print_subseq_n_ball_numbers()
        # TODO: subsequence and month
        self.subseq_n_month = self.print_subseq_n_month_numbers()
        # TODO: subsequence and day
        self.subseq_n_day = self.print_subseq_n_day_numbers()

        # ---------- Date Combinations
        # TODO: date and frequented
        self.date_n_freq = self.print_date_n_freq_numbers()
        # TODO: date and missing
        self.date_n_missn = self.print_date_n_missn_numbers()
        # duplicatedTODO: subsequence and date
        # TODO: date and ball
        self.date_n_ball = self.print_date_n_ball_numbers()
        # TODO: date and month
        self.date_n_month = self.print_date_n_month_numbers()
        # TODO: date and day
        self.date_n_day = self.print_date_n_day_numbers()

        # ---------- Ball Combinations
        # TODO: ball and frequented
        self.ball_n_freq = self.print_ball_n_freq_numbers()
        # TODO: ball and missing
        self.ball_n_missn = self.print_ball_n_missn_numbers()
        # duplicatedTODO: subsequence and ball
        # duplicatedTODO: date and ball
        # TODO: ball and month
        self.ball_n_month = self.print_ball_n_month_numbers()
        # TODO: ball and day
        self.ball_n_day = self.print_ball_n_day_numbers()

        # ---------- Month Combinations
        # TODO: month and frequented
        self.month_n_freq = self.print_month_n_freq_numbers()
        # TODO: month and missing
        self.month_n_missn = self.print_month_n_missn_numbers()
        # duplicatedTODO: subsequence and month
        # duplicatedTODO: date and month
        # duplicatedTODO: ball and month
        # TODO: month and day
        self.month_n_day = self.print_month_n_day_numbers()

        # ---------- Day Combinations
        # TODO: day and frequented
        self.day_n_freq = self.print_day_n_freq_numbers()
        # TODO: day and missing
        self.day_n_missn = self.print_day_n_missn_numbers()
        # duplicatedTODO: subsequence and day
        # duplicatedTODO: date and day
        # duplicatedTODO: ball and day
        # duplicatedTODO: month and day

        # ---------- Multi Combinations: date, month, day, + Subsequence
        self.date_month_day_subseq = self.print_date_month_day_subseq()

        pick = 6
        Contents.print_tickets(pick, self.date_month_day_subseq)

        self.grand_group_numbers = self.get_collection_of_all_numbers()

        pick = 6
        Contents.print_tickets(pick, self.grand_group_numbers)

    @staticmethod
    def print_title(title):
        print("")
        print(f"===== {title} =====")

    @staticmethod
    def print_seperator():
        print(f"-------------------------------")

    def print_info_last_draw(self):
        print(f"TODAY: {self.today}")
        Contents.print_seperator()
        # draw id, date, time, day, month, drawn numbers
        Contents.print_title("LAST DRAW IN DATABASE")
        print(f"LAST DRAW ID: {self.service.last_draw_id}")
        last_draw_date_short = self.service.last_draw_date.strftime("%Y-%B-%d")
        # month_last_draw = utils.get_month_of_year(self.service.last_draw_date)
        day_last_draw = utils.get_day_of_week(self.service.last_draw_date).upper()
        print(f"LAST DRAW DATE: {last_draw_date_short} - {day_last_draw}")
        print(f"LAST DRAW NUMBERS: {self.service.last_draw_numbers}")
        # Contents.print_seperator()

    def print_info_next_draw(self):
        # next draw (date, time, day, month)
        Contents.print_title("NEXT DRAW")
        next_draw_timestamp = utils.get_future_draw_date()[0].strftime("%Y-%B-%d")
        # next_draw_month = self.service.next_draw_month
        next_draw_day = self.service.next_draw_day.upper()
        print(f"NEXT DRAW DATE: {next_draw_timestamp} - {next_draw_day}")

    def print_repetitions_stats(self):
        Contents.print_title("REPETITIONS")
        print(f"Total number of repetitions: {self.repetitions_stats['total_repetitions']}")
        repeated_numbers = self.repetitions_stats['repeated_nums']
        repeated_numbers_to_list = utils.convert_string_to_list_of_numbers(repeated_numbers)
        print(f"Repeated Numbers : {repeated_numbers_to_list}")

    def print_freq_and_missn_stats(self):
        Contents.print_title("FREQUENTED & MISSED NUMBERS")
        # In the last 20 draws, if a number has more than 7 frequency, but not drawn in last 5 draws, then chance is higher for that number
        freq_nums = utils.convert_string_to_list_of_numbers(self.freq_and_missn_stats['frequented_nums'])
        freq_pool_size = rep_freq_miss_queries.pool_size_frequented
        missing_nums = utils.convert_string_to_list_of_numbers(self.freq_and_missn_stats['missing_nums'])
        missing_pool_size = rep_freq_miss_queries.pool_size_missing
        freq_n_missed_nums = utils.convert_string_to_list_of_numbers(self.freq_and_missn_stats['freq_and_missing'])
        print(f"Frequented Numbers in 'Last {freq_pool_size}' Draws: {freq_nums}")
        print(f"Missed Numbers  in 'Last {missing_pool_size}' Draws: {missing_nums}")
        print(f"Frequented but Missed Numbers : {freq_n_missed_nums}")
        return freq_nums, missing_nums

    @staticmethod
    def is_drawn_number_in_collection(drawn_numbers, collection):
        found_in_collection = []
        for drawn_number in drawn_numbers:
            if drawn_number in collection:
                found_in_collection.append(drawn_number)
        return found_in_collection

    def print_subsequence_stats(self):
        Contents.print_title("SUBSEQUENCE NUMBERS")
        subsequence_numbers_highest_freq = []
        for ball, subseq_dict in self.subsequence_stats.items():
            print(f"{ball}: {subseq_dict}")
            subsequence_numbers_highest_freq.append(subseq_dict[0]['subseq_num'])
        # print(f"Subsequence Numbers (with the highest freq): {subsequence_numbers_highest_freq}")
        subsequence_numbers_highest_freq = subsequence_numbers_highest_freq[: collectn_size]
        print(subsequence_numbers_highest_freq)
        print(f"Total Numbers in collection: {len(subsequence_numbers_highest_freq)}")
        numbers_found = Contents.is_drawn_number_in_collection(self.drawn_numbers, subsequence_numbers_highest_freq)
        print(f"{len(numbers_found)} Numbers Found: {numbers_found}")
        print(f"Drawn: {self.drawn_numbers}")
        return subsequence_numbers_highest_freq

    def print_freq_by_date_stats(self):
        Contents.print_title("FREQUENTED NUMBERS BY DATE")
        freq_by_date_numbers = list(self.freq_by_date_stats.keys())[: collectn_size]
        # print(f"Frequented Numbers By Date (with the highest freq): {freq_by_date_numbers}")
        print(freq_by_date_numbers)
        print(f"Total Numbers in collection: {len(freq_by_date_numbers)}")
        numbers_found = Contents.is_drawn_number_in_collection(self.drawn_numbers, freq_by_date_numbers)
        print(f"{len(numbers_found)} Numbers Found: {numbers_found}")
        return freq_by_date_numbers

    def print_freq_by_ball_stats(self):
        Contents.print_title("FREQUENTED NUMBERS BY BALL")
        freq_by_ball_numbers_highest_freq = []
        for ball, drawn_num_dict in self.freq_by_ball_stats.items():
            # print(f"{ball}: {drawn_num_dict[0]['drawn_num']}")
            freq_by_ball_numbers_highest_freq.append(drawn_num_dict[0]['drawn_num'])
        # print(f"Frequented Numbers By Ball (with the highest freq): {freq_by_ball_numbers_highest_freq}")
        freq_by_ball_numbers_highest_freq = freq_by_ball_numbers_highest_freq[: collectn_size]
        print(freq_by_ball_numbers_highest_freq)
        print(f"Total Numbers in collection: {len(freq_by_ball_numbers_highest_freq)}")
        numbers_found = Contents.is_drawn_number_in_collection(self.drawn_numbers, freq_by_ball_numbers_highest_freq)
        print(f"{len(numbers_found)} Numbers Found: {numbers_found}")
        return freq_by_ball_numbers_highest_freq

    def print_freq_by_month_stats(self):
        Contents.print_title("FREQUENTED NUMBERS BY MONTH")
        freq_by_month_numbers = list(self.freq_by_month_stats.keys())[:collectn_size]
        # print(f"Frequented Numbers By Month (with the highest freq): {freq_by_month_numbers}")
        print(freq_by_month_numbers)
        print(f"Total Numbers in collection: {len(freq_by_month_numbers)}")
        numbers_found = Contents.is_drawn_number_in_collection(self.drawn_numbers, freq_by_month_numbers)
        print(f"{len(numbers_found)} Numbers Found: {numbers_found}")
        return freq_by_month_numbers

    def print_freq_by_day_stats(self):
        Contents.print_title("FREQUENTED NUMBERS BY DAY")
        freq_by_day_numbers = list(self.freq_by_day_stats.keys())[:collectn_size]
        # print(f"Frequented Numbers By Day (with the highest freq): {freq_by_day_numbers}")
        print(freq_by_day_numbers)
        print(f"Total Numbers in collection: {len(freq_by_day_numbers)}")
        numbers_found = Contents.is_drawn_number_in_collection(self.drawn_numbers, freq_by_day_numbers)
        print(f"{len(numbers_found)} Numbers Found: {numbers_found}")
        return freq_by_day_numbers

    def print_subseq_n_freq_numbers(self):
        title = "SUBSEQUENCE and FREQUENTED NUMBERS"
        collection1 = self.subseq_numbers
        collection2 = self.freq_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_subseq_n_missn_numbers(self):
        title = "SUBSEQUENCE and MISSING NUMBERS"
        collection1 = self.subseq_numbers
        collection2 = self.missn_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_subseq_n_date_numbers(self):
        title = "SUBSEQUENCE and DATE NUMBERS"
        collection1 = self.subseq_numbers
        collection2 = self.date_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_subseq_n_ball_numbers(self):
        title = "SUBSEQUENCE and BALL NUMBERS"
        collection1 = self.subseq_numbers
        collection2 = self.ball_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_subseq_n_month_numbers(self):
        title = "SUBSEQUENCE and MONTH NUMBERS"
        collection1 = self.subseq_numbers
        collection2 = self.month_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_subseq_n_day_numbers(self):
        title = "SUBSEQUENCE and DAY NUMBERS"
        collection1 = self.subseq_numbers
        collection2 = self.day_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    # ---------- Date Combinations
    def print_date_n_freq_numbers(self):
        title = "DATE and FREQUENTED NUMBERS"
        collection1 = self.date_numbers
        collection2 = self.freq_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_date_n_missn_numbers(self):
        title = "DATE and MISSING NUMBERS"
        collection1 = self.date_numbers
        collection2 = self.missn_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_date_n_ball_numbers(self):
        title = "DATE and BALL NUMBERS"
        collection1 = self.date_numbers
        collection2 = self.ball_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_date_n_month_numbers(self):
        title = "DATE and MONTH NUMBERS"
        collection1 = self.date_numbers
        collection2 = self.month_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_date_n_day_numbers(self):
        title = "DATE and DAY NUMBERS"
        collection1 = self.date_numbers
        collection2 = self.day_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    # ---------- Ball Combinations
    def print_ball_n_freq_numbers(self):
        title = "BALL and FREQUENTED NUMBERS"
        collection1 = self.ball_numbers
        collection2 = self.freq_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_ball_n_missn_numbers(self):
        title = "BALL and MISSING NUMBERS"
        collection1 = self.ball_numbers
        collection2 = self.missn_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_ball_n_month_numbers(self):
        title = "BALL and MONTH NUMBERS"
        collection1 = self.ball_numbers
        collection2 = self.month_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_ball_n_day_numbers(self):
        title = "BALL and DAY NUMBERS"
        collection1 = self.ball_numbers
        collection2 = self.day_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    # ---------- Month Combinations
    def print_month_n_freq_numbers(self):
        title = "MONTH and FREQUENTED NUMBERS"
        collection1 = self.month_numbers
        collection2 = self.freq_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_month_n_missn_numbers(self):
        title = "MONTH and MISSING NUMBERS"
        collection1 = self.month_numbers
        collection2 = self.missn_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_month_n_day_numbers(self):
        title = "MONTH and DAY NUMBERS"
        collection1 = self.month_numbers
        collection2 = self.day_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)


    # ---------- Day Combinations
    def print_day_n_freq_numbers(self):
        title = "DAY and FREQUENTED NUMBERS"
        collection1 = self.day_numbers
        collection2 = self.freq_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

    def print_day_n_missn_numbers(self):
        title = "DAY and MISSING NUMBERS"
        collection1 = self.day_numbers
        collection2 = self.missn_numbers
        return Contents.print_combined_numbers(title, collection1, collection2)

# ----------------------------------------------------------------

    @staticmethod
    def print_combined_numbers(title, collection1, collection2):
        Contents.print_title(title)
        collected_numbers = []
        collected_numbers.extend(collection1)
        collected_numbers.extend(collection2)
        unsorted_dict = utils.create_dict_collection(collected_numbers)
        sorted_dict = utils.sorted_dict_by_value(unsorted_dict)
        # print(sorted_dict)
        combined_numbers_list = list(sorted_dict.keys())[:collectn_size]
        print(combined_numbers_list)
        print(f"Total Numbers in collection: {len(combined_numbers_list)}")
        numbers_found = Contents.is_drawn_number_in_collection(drawn_numbers, combined_numbers_list)
        print(f"{len(numbers_found)} Numbers Found: {numbers_found}")
        return combined_numbers_list

    def get_collection_of_all_numbers(self):
        Contents.print_title("Collection of all numbers")
        group = []
        group.extend(self.subseq_numbers)
        group.extend(self.freq_numbers)
        group.extend(self.missn_numbers)
        group.extend(self.date_numbers)
        group.extend(self.ball_numbers)
        group.extend(self.month_numbers)
        group.extend(self.day_numbers)
        group_freq_dict = utils.create_dict_collection(group)
        sorted_group = utils.sorted_dict_by_value(group_freq_dict)
        print(sorted_group)
        final_group = list(sorted_group.keys())
        print(f"{len(final_group)}")
        print(final_group)
        return final_group

    def print_date_month_day_subseq(self):
        # collection of most frequented numbers for each criteria,
        # then take most frequented within this group
        Contents.print_title("Combined Numbers : date + month + day + subseq")
        group = []
        group.extend(self.subseq_numbers)
        group.extend(self.date_numbers)
        group.extend(self.month_numbers)
        group.extend(self.day_numbers)
        group_freq_dict = utils.create_dict_collection(group)
        sorted_group = utils.sorted_dict_by_value(group_freq_dict)
        print(sorted_group)
        final_group = list(sorted_group.keys())
        print(f"{len(final_group)}")
        print(final_group)
        return final_group


    @staticmethod
    def print_tickets(pick, group_of_numbers):
        count = 0
        for number in group_of_numbers:
            print(number)
            count += 1
            if count % pick == 0:
                print(f"---pick of {pick}")
