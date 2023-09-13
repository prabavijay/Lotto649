"""
class to provide basic DB queries to read data from various tables
1) get last row id
2) get last draw results
3) get draw results for N draws
"""


class BasicQueries:

    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.last_draw_id = self.get_id_from_last_draw()
        self.second_last_draw_id = self.get_id_from_second_last_draw()
        self.last_drawn_numbers = self.get_last_draw_results()
        self.second_last_drawn_numbers = self.get_second_last_draw_results()
        self.n_draws_results = None

    def get_id_from_last_draw(self):
        sql = "SELECT MAX(id) FROM draw_results;"
        return self.db_connect.run_sql_statement(sql)[0][0]

    def get_id_from_second_last_draw(self):
        sql = "SELECT id From (select id from draw_results dr ORDER BY id  DESC LIMIT 2) AS second_last ORDER BY id LIMIT 1;"
        return self.db_connect.run_sql_statement(sql)[0][0]

    # Get list of row IDs from entire table
    def get_list_of_row_ids(self, table='draw_results'):
        sql = f"SELECT id FROM {table};"
        result = self.db_connect.run_sql_statement(sql)
        id_list = []
        for id in result:
            id_list.append(int(id[0]))
        return id_list

    def get_last_draw_results(self):
        return self.get_draw_results_by_id(self.last_draw_id)

    def get_second_last_draw_results(self):
        return self.get_draw_results_by_id(self.second_last_draw_id)

    def get_draw_results_by_id(self, row_id):
        sql = f"SELECT * from draw_results where id = {row_id}"
        result = self.db_connect.run_sql_statement(sql)
        drawn_numbers = result[0][2:]
        return drawn_numbers

    def get_n_draws_results(self, from_row_id, pool_size=20):
        sql = f"SELECT  * FROM draw_results WHERE id <= {from_row_id} ORDER BY id DESC LIMIT {pool_size}"
        result = self.db_connect.run_sql_statement(sql)
        print(f"result set size = {len(result)}")
        drawn_numbers = result
        return drawn_numbers

    def get_draw_date_numbers_by_id(self, draw_id):
        sql = f"SELECT * from draw_results where id = {draw_id}"
        result = self.db_connect.run_sql_statement(sql)
        draw_date = result[0][1]
        draw_numbers = result[0][2:]
        return draw_date, draw_numbers

    def get_id_from_table(self, table_name):
        sql = f"SELECT MAX(id) FROM {table_name};"
        return self.db_connect.run_sql_statement(sql)[0][0]

    def get_last_processed_id_from_stats_tracker(self, stats_table_name):
        sql = f"SELECT draw_processed from stats_tracker where stats_table = '{stats_table_name}'"
        result = self.db_connect.run_sql_statement(sql)
        draw_processed = result[0][0]
        return draw_processed

    def get_data_from_stats_table(self, stats_table_name, stats_table_id):
        sql = f"SELECT * from {stats_table_name} where id = '{stats_table_id}'"
        result = self.db_connect.run_sql_statement(sql)
        return result[0]

    def get_data_from_freq_by_table(self, table_name, filter_by, limit):
        # # select drawn_number, date_3 from freq_by_date order by date_3 desc limit 10;
        sql = f"SELECT drawn_number, {filter_by} from {table_name} order by {filter_by} desc limit {limit}"
        result = self.db_connect.run_sql_statement(sql)
        return result

    def get_most_frequented_subsequence_numbes(self, ball_number, base_number, limit=5):
        # select subseq_num, frequency from subsequence s where s.ball_num = 1 and base_num = 4 order by frequency desc limit 10;
        sql = f"SELECT subseq_num, frequency from subsequence s where s.ball_num = {ball_number} and base_num = {base_number} order by frequency desc limit {limit}"
        result = self.db_connect.run_sql_statement(sql)
        return result