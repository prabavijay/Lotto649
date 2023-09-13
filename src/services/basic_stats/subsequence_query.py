from itertools import islice
import src.utils as utils
from src.services.dba.db_queries import BasicQueries


# from src.reporter import Reporter
# from src.data_importer import DataImporter


class SubsequenceQuery:

    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.basic_queries = BasicQueries(self.db_connect)
        self.last_draw_id = self.basic_queries.last_draw_id
        self.positions_dict = utils.build_subseq_by_position_structure()
        self.base_freq_dict = utils.build_freq_by_position_structure()
        self.subsequence_numbers = None

    def get_subsequence_numbers(self):
        ball_num_dict_unsorted = self.build_subsequence_numbers()
        return ball_num_dict_unsorted
        # ball_num_dict = {}
        # for ball, base_dict in ball_num_dict_unsorted.items():
        #     # {ball_1: {base_num_1: {subseq_num_1: 22}}}, {ball_2: {base_num_2: {sub}}}
        #     for base, subseq_num_dict in base_dict.items():
        #         sorted_subseq_num_dict = SubsequenceQuery.sort_subsequence_by_frequency(subseq_num_dict)
        #         if not bool(sorted_subseq_num_dict):
        #             ball_num_dict_unsorted[ball][base] = sorted_subseq_num_dict
        #             print(f"Subsequence sorted for Ball {ball} ====> {ball_num_dict_unsorted[ball][base]}")
        # self.subsequence_stats = ball_num_dict_unsorted
        # return ball_num_dict_unsorted

    @staticmethod
    def sort_subsequence_by_frequency(subseq_dict):
        sorted_subseq_by_freq = sorted(subseq_dict.items(), key=lambda x: x[1], reverse=True)
        converted_dict = dict(sorted_subseq_by_freq)
        zero_freq_removed_dict = {key:value for (key, value) in converted_dict.items() if value != 0}
        return zero_freq_removed_dict

    def build_subsequence_numbers(self):
        ball_dict = utils.create_dict_of_balls()

        # 1) get list of draws IDs
        row_ids = self.basic_queries.get_list_of_row_ids()
        total_id = len(row_ids)
        last_draw_id = row_ids[-1]

        # 2) get draw numbers from base_draw
        for id in row_ids:
            base_draw_id = id
            if base_draw_id == last_draw_id:
                break
            id_index_in_ids = row_ids.index(base_draw_id)
            base_draw = self.basic_queries.get_draw_results_by_id(base_draw_id)

            # 3) get draw numbers from subseq_draw
            subseq_draw_id = row_ids[id_index_in_ids + 1]
            subseq_draw = self.basic_queries.get_draw_results_by_id(subseq_draw_id)

            # 4) for each base_draw_number in base_draw build subseq_num_dict
            ball_index = 0

            for base_number in base_draw:
                subseq_number_processing = subseq_draw[ball_index] # both draws indexed by zero-based ball index
                # for current_ball, first find base number, then subseq number, then update frequency
                ball_index += 1 # increment
                ball_dict[ball_index][base_number][subseq_number_processing] += 1
        return ball_dict

    @staticmethod
    def sort_nested_keys_by_freq_ss(subseq_num_dict_unsorted):
        # Sort Nested keys by Value
        sorted_by_freq_dict = {key: dict(sorted(val.items(), key=lambda ele: ele[1], reverse=True))
               for key, val in subseq_num_dict_unsorted.items()}
        return sorted_by_freq_dict
    # ----------------------------------------------------------------
    # TODO: see if following 4 functions can be done in SQL
    def remove_extra_keys_with_low_freq(self, freq_min=5):
        """Remove unwanted/extra keys from base_numbers, ss_numbers by Position if values are Zeros"""
        for position, base_numbers_ss_numbers in self.positions_dict.items():
            remove_base_id = []
            for base_numbers, ss_numbers in base_numbers_ss_numbers.items():
                remove_ss_id = []
                for ss_number, freq in ss_numbers.items():
                    if freq < freq_min:
                        remove_ss_id.append(ss_number)
                for id in remove_ss_id:
                    del ss_numbers[id]
                if len(ss_numbers) == 0:
                    remove_base_id.append(base_numbers)

            for id in remove_base_id:
                del base_numbers_ss_numbers[id]
                # print(f"Position: {position}, Base_Number: {base_numbers}")
                # print(f"SS to Remove: {remove_ss_id_list}")

    @staticmethod
    def take_n_items(set_limit, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, set_limit))

    def get_top_n_base_numbers(self, sorted_by_freq_dict, set_limit=3):
        pos_dict = {}
        top_3_list = []
        # for position, base_numbers_ss_numbers in sorted_by_freq_dict.items():
        base_dict = {}
        for position, base_dict in sorted_by_freq_dict.items():
                n_items = SubsequenceQuery.take_n_items(set_limit, base_dict.items())

                # print(position, base_dict, n_items)
                base_dict = dict(n_items)
                # top_3_list.append([position, base_numbers, n_items])
                pos_dict[position] = base_dict
        return pos_dict

    def get_top_n_subsequence_numbers(self, sorted_by_freq_dict, set_limit=3):
        pos_dict = {}
        top_3_list = []
        for position, base_numbers_ss_numbers in sorted_by_freq_dict.items():
            base_dict = {}
            for base_numbers, ss_numbers in base_numbers_ss_numbers.items():
                    n_items = SubsequenceQuery.take_n_items(set_limit, ss_numbers.items())

                    # print(position, base_numbers, n_items)
                    ss_dict = dict(n_items)
                    top_3_list.append([position, base_numbers, n_items])
                    base_dict[base_numbers] = ss_dict
            pos_dict[position] = base_dict
        return pos_dict
