import sqlalchemy as db

from src.services.dba.create_drop_tables import TableCreateDrop
from src.services.dba.db_model import FreqByBall, FreqByMonth, FreqByDay, FreqByDate, Subsequence, \
    Repetition, FreqAndMissing, StatsTracker
from src.services.dba.db_queries import BasicQueries


class BasicStatsUpdater:
    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.basic_queries = BasicQueries(self.db_connect)
        self.last_draw_id = self.basic_queries.last_draw_id

    def update_stats_tracker(self, stats_table_name):
        self.db_connect.session.query(StatsTracker).filter_by(stats_table=stats_table_name) \
            .update({'draw_processed': self.last_draw_id})
        self.db_connect.session.commit()

    def update_freq_by_balls(self, freq_by_balls):
        print("***** Updating Freq. by Balls ...")
        for key, value in freq_by_balls.items():
            for base_number, frequency in value.items():
                # print(base_number, frequency)
                self.db_connect.session.query(FreqByBall).filter_by(drawn_number=base_number) \
                    .update({key: frequency})
                self.db_connect.session.commit()
        self.update_stats_tracker('freq_by_ball')

    def update_freq_by_months(self, freq_by_months):
        print("***** Updating Freq. by Months ...")
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        for key, value in freq_by_months.items():
            for base_number, frequency in value.items():
                # print(base_number, frequency)
                self.db_connect.session.query(FreqByMonth).filter_by(drawn_number=base_number) \
                    .update({months[key - 1]: frequency})
                self.db_connect.session.commit()
        self.update_stats_tracker('freq_by_month')

    def update_freq_by_days(self, freq_by_days):
        print("***** Updating Freq. by Days ...")

        for key, value in freq_by_days.items():
            for base_number, frequency in value.items():
                # print(base_number, frequency)
                self.db_connect.session.query(FreqByDay).filter_by(drawn_number=base_number) \
                    .update({key: frequency})
                self.db_connect.session.commit()
        self.update_stats_tracker('freq_by_day')

    def update_freq_by_dates(self, freq_by_dates):
        print("***** Updating Freq. by Dates ...")

        for key, value in freq_by_dates.items():
            for base_number, frequency in value.items():
                column_name = 'date_' + str(key)
                # print(base_number, frequency)
                self.db_connect.session.query(FreqByDate).filter_by(drawn_number=base_number) \
                    .update({column_name: frequency})
                self.db_connect.session.commit()
        self.update_stats_tracker('freq_by_date')

    def update_subsequence_numbers(self, subseq_root_dict):
        print("***** updating frequency into Subsequence ...")

        for ball_number, base_num_dict in subseq_root_dict.items():
            for base_number, subseq_num_dict in base_num_dict.items():
                for subseq_number, freq in subseq_num_dict.items():
                    # data_to_insert = Subsequence(ball_num, base_num, subseq_num, frequency)
                    # self.db_connect.session.add(data_to_insert)
                    if freq > 0:
                        (self.db_connect.session.query(Subsequence).filter(Subsequence.ball_num == ball_number,
                                                                           Subsequence.base_num == base_number,
                                                                           Subsequence.subseq_num == subseq_number).update({Subsequence.frequency: freq}))
        # commit and close session
        self.db_connect.session.commit()
        self.update_stats_tracker('subsequence')

    def bulk_insert_subsequence_numbers(self, subseq_root_dict):
        print("***** bulk inserting into Subsequence ...")
        # self.db_connect.session.query(Subsequence).delete()
        table_recreate = TableCreateDrop()
        table_recreate.drop_table(Subsequence.__table__)
        table_recreate.create_table(Subsequence.__table__)

        for ball_num, base_num_dict in subseq_root_dict.items():
            for base_num, subseq_num_dict in base_num_dict.items():
                for subseq_num, frequency in subseq_num_dict.items():
                    if frequency > 0:
                        data_to_insert = Subsequence(ball_num, base_num, subseq_num, frequency)
                        self.db_connect.session.add(data_to_insert)
        # commit and close session
        self.db_connect.session.commit()
        self.update_stats_tracker('subsequence')

    def update_repetition_stats(self, repetition_stats):
        print("***** Updating repetition stats ...")
        table_recreate = TableCreateDrop()
        table_recreate.drop_table(Repetition.__table__)
        table_recreate.create_table(Repetition.__table__)

        for item in repetition_stats:
            base_draw_id = item[0]
            draw_date = item[1]
            repeated_nums = item[2]
            repeated_balls = item[3]
            total_repeated = item[4]
            data_to_insert = Repetition(base_draw_id, draw_date, repeated_nums, repeated_balls, total_repeated)
            self.db_connect.session.add(data_to_insert)
        self.db_connect.session.commit()
        self.update_stats_tracker('repetition')

    def update_freq_and_missing_stats(self, freq_missn_stats):
        print("***** Updating Freq. and Missing stats ...")
        last_draw_id = freq_missn_stats['id']
        draw_date = freq_missn_stats['draw_date']
        missing = freq_missn_stats['missing']
        frequented = []
        for number, frequency in freq_missn_stats['frequented'].items():
            if frequency >= 5:
                frequented.append(number)
        freq_but_missing = freq_missn_stats['freq_but_missing']

        data_to_insert = FreqAndMissing(last_draw_id, draw_date, frequented, missing, freq_but_missing)
        self.db_connect.session.add(data_to_insert)
        self.db_connect.session.commit()
        self.update_stats_tracker('freq_and_missn')
