from src import utils


balls_list = utils.get_list_of_balls()
balls_list_string = utils.convert_list_of_balls_to_string(balls_list)


class FrequentByQueries:
    def __init__(self, db_connect):
        self.db_connect = db_connect

    def get_freq_by_specific_ball(self, ball_num=1):
        self.get_freq_by_ball_number('ball_' + str(ball_num))

    def get_freq_by_balls(self):
        dict_freq_by_balls = {}
        for ball_number in range(1, 8):
            str_ball_number = 'ball_' + str(ball_number)
            result = self.get_freq_by_ball_number(str_ball_number)
            # converting list to dict : [[48, 1], ..., [50, 1]] --> {48:1, ..., 50:1}
            dict_freq_by_specific_ball = {}
            for item in result:
                dict_freq_by_specific_ball[item[0]] = item[1]
            dict_freq_by_balls[str_ball_number] = dict_freq_by_specific_ball
        return dict_freq_by_balls

    def get_freq_by_ball_number(self, ball_number='ball_1'):
        # -- ********** CASE 2: BaseNumbers, frequented in ball_20
        # select ball_20, count(ball_20) from draw_results group by ball_20 order by ball_20 asc
        # /*
        # ball_20|count|
        # ------+-----+
        #     48|    1|
        #     49|    2|
        #     50|    1|
        #     68| 2176|
        #     69| 2819|
        #     70| 3951|
        sql = f"select {ball_number}, count({ball_number}) from draw_results group by {ball_number} order by {ball_number} asc"
        result = self.db_connect.run_sql_statement(sql)
        # for record in result:
        #     print(f"Frequency By Ball Number {ball_number}: {record}")
        return result

    def get_freq_by_months(self):
        dict_freq_by_months = {}
        for month in range(1, 13):
            result = self.get_freq_by_specific_month(month)
            dict_freq_by_months[month] = result
        return dict_freq_by_months

    def get_freq_by_specific_month(self, month=1):
        dict_freq_by_specific_month = {}
        for base_number in range(1, 50):
            result = self.get_freq_by_month_and_base_number(base_number, month)
            dict_freq_by_specific_month[base_number] = result
        return dict_freq_by_specific_month

    def get_freq_by_month_and_base_number(self, base_num, month=1):
        # -- ********** CASE 3: BaseNum = 10, frequented by = month
        # select 10 as num, to_char(draw_date, 'month') as month_name, count(draw_date)  from draw_results where 10 in (ball_1,ball_2,ball_3,ball_4,ball_5,ball_6,ball_7,ball_8,ball_9,ball_10) and EXTRACT(MONTH FROM draw_date) = 10 group by month_name;
        # --num|month_name|count|
        # -----+----------+-----+
        # -- 10|october   |  334|
        # sql = (f"select {base_num}, to_char(draw_date, 'month') as month_name, count(draw_date) from draw_results where"
        #        f" {base_num} in ({balls_list_string})  and EXTRACT(MONTH FROM draw_date) = {month} group by month_name;")
        sql = (f"select {base_num}, to_char(draw_date, 'month') as month_name, count(draw_date) from draw_results where"
               f" {base_num} in ({balls_list_string})  and EXTRACT(MONTH FROM draw_date) = {month} group by month_name;")
        result = self.db_connect.run_sql_statement(sql)[0][2]
        # for record in result:
        #     print(f"Frequency By Month: {record}")
        return result

    def get_freq_by_days(self):
        dict_freq_by_days = {}
        for day in ['wed', 'sat']:
            result = self.get_freq_by_specific_day(day)
            dict_freq_by_days[day] = result
        return dict_freq_by_days

    def get_freq_by_specific_day(self, day='sat'):
        dict_freq_by_specific_day = {}
        for base_number in range(1, 50):
            result = self.get_freq_by_day_and_base_number(base_number, day)
            dict_freq_by_specific_day[base_number] = result
        return dict_freq_by_specific_day

    def get_freq_by_day_and_base_number(self, base_num, day):
        # -- ********** CASE 5: BaseNum = 10, frequented by = day_name
        # select 10 as num, to_char(draw_date, 'day') as day_name, count(draw_date) from draw_results where 10 in (ball_1,ball_2) group by day_name
        # --num|day_name |count|
        # -----+---------+-----+
        # -- 10|monday   |  129|
        # -- 10|thursday |  125|
        # -- 10|tuesday  |  124|
        # -- 10|saturday |  129|
        # -- 10|sunday   |  127|
        # -- 10|friday   |  129|
        # -- 10|wednesday|  120|
        # sql = (f"select {base_num}, to_char(draw_date, 'day') as day_name, count(draw_date) from draw_results where"
        #        f" {base_num} in ({balls_list_string}) group by day_name;")
        sql = (f"select * from (select {base_num}, to_char(draw_date, 'day') as day_name, "
               f"count(to_char(draw_date, 'day')) from draw_results where {base_num} in ({balls_list_string}) "
               f"group by to_char(draw_date, 'day')) as main where main.day_name like '{day}%'")
        result = self.db_connect.run_sql_statement(sql)[0][2]
        # for record in result:
        #     print(f"Frequency By Day: {record}")
        #     if str(record[1].strip()) == 'monday':
        #         print(f"Frequency By Day {day}: {record[0]}, {record[1]}, {record[2]}")
        return result

    def get_freq_by_dates_of_month(self):
        dict_freq_by_dates = {}
        for date_of_month in range(1, 32):
            result = self.get_freq_by_specific_date_of_month(date_of_month)
            dict_freq_by_dates[date_of_month] = result
        return dict_freq_by_dates

    def get_freq_by_specific_date_of_month(self, date_of_month=31):
        dict_freq_by_specific_date_of_month = {}
        for base_number in range(1, 50):
            result = self.get_freq_by_date_and_base_number(base_number, date_of_month)
            dict_freq_by_specific_date_of_month[base_number] = result
        return dict_freq_by_specific_date_of_month

    def get_freq_by_date_and_base_number(self, base_num, date_of_month=31):
        # -- ********** CASE 3: BaseNum = 10, frequented by = date of month
        # select 10 as num, EXTRACT(DAY FROM draw_date) as date_of_month, count(draw_date)  from draw_results where 10 in (ball_1,ball_2,ball_3,ball_4,ball_5,ball_6,ball_7,ball_8,ball_9,ball_10) and EXTRACT(DAY FROM draw_date) = 31 group by date_of_month;        # --num|month_name|count|
        # num|date_of_month|count|
        # ---+-------------+-----+
        #  10|           31|   73|
        sql = (f"select {base_num}, EXTRACT(DAY FROM draw_date) as date_of_month, count(draw_date) from draw_results where"
               f" {base_num} in ({balls_list_string}) and EXTRACT(DAY FROM draw_date) = {date_of_month} group by date_of_month;")
        result = self.db_connect.run_sql_statement(sql)[0][2]
        # for record in result:
        #     print(f"Frequency By Date: {record}")
        return result
