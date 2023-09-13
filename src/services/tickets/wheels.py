import src.utils as utils

class Wheel:
    def __init__(self, db_connect, stats):
        self.db_connect = db_connect
        self. collected_numbers = Wheel.collect_numbers_from_stats(stats)
        self.collected_numbers_expanded = Wheel.collected_numbers_expanded(self. collected_numbers)
        self.size_collection = len(self.collected_numbers_expanded)
        print(f"Size of collected numbers: {self.size_collection}")
        self.freq_in_collection = Wheel.create_dict_freq_in_collection(self.collected_numbers_expanded)
        self.collection_sorted = Wheel.sorted_dict_by_value(self.freq_in_collection)
        Wheel.print_group_of_10s(self.collection_sorted)

    @staticmethod
    def print_group_of_10s(collection):
        count = 0
        for key in collection.keys():
            print(key)
            count += 1
            if count % 10 == 0:
                print("------")
    @staticmethod
    def create_dict_freq_in_collection(numbers_list):
        collection_dict = {}
        for num in numbers_list:
            if num not in collection_dict.keys():
                collection_dict[num] = 1
            else:
                collection_dict[num] += 1
        # print(collection_dict)
        return collection_dict

    @staticmethod
    def sorted_dict_by_value(unsorted_dict):
        sorted_by_freq = sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True)
        converted_dict = dict(sorted_by_freq)
        print(converted_dict)
        return converted_dict
    @staticmethod
    def collect_numbers_from_stats(stats):
        str_repetition_nums = stats['repetition_stats']['repeated_nums']
        repetition_nums = utils.convert_string_to_list_of_numbers(str_repetition_nums)
        str_freq_and_missd_nums = stats['freq_and_missn_stats']['freq_and_missing']
        freq_and_missd_nums = utils.convert_string_to_list_of_numbers(str_freq_and_missd_nums)
        freq_by_date = list(stats['freq_by_date_stats'].keys())
        freq_by_month = list(stats['freq_by_month_stats'].keys())
        freq_by_day = list(stats['freq_by_day_stats'].keys())
        freq_by_ball_stats = stats['freq_by_ball_stats']
        freq_by_ball_dict = Wheel.drawn_numbers_dict_by_ball(freq_by_ball_stats)
        freq_by_ball = Wheel.extract_drawn_numbers(freq_by_ball_dict)
        collected_numbers = [freq_and_missd_nums, freq_by_date,
                             freq_by_month, freq_by_day, freq_by_ball]
        return collected_numbers

    @staticmethod
    def extract_drawn_numbers(freq_by_ball_dict):
        drawn_numbers = []
        for ball, drawn_numbers in freq_by_ball_dict.items():
            drawn_numbers.extend(drawn_numbers)
        return drawn_numbers

    @staticmethod
    def drawn_numbers_dict_by_ball(stats_dict):
        freq_by_ball = {}
        for ball, drawn_num_list in stats_dict.items():
            drawn_num_by_ball = []
            for drawn_num_dict in drawn_num_list:
                # print(drawn_num_dict['drawn_num'])
                drawn_num_by_ball.append(drawn_num_dict['drawn_num'])
            freq_by_ball[ball] = drawn_num_by_ball
        return freq_by_ball

    @staticmethod
    def collected_numbers_expanded(collected_numbers):
        expanded = []
        for sublist in collected_numbers:
            expanded.extend(sublist)
        return expanded


