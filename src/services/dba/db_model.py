import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, INT, SMALLINT, DATE, TIME, Integer, String, ForeignKey, func, text)

Base = declarative_base()


class DrawResults(Base):
    __tablename__ = 'draw_results'

    id = Column(db.INT, primary_key=True)
    draw_date = Column(db.DATE, nullable=False)
    ball_1 = Column(SMALLINT, nullable=False)
    ball_2 = Column(SMALLINT, nullable=False)
    ball_3 = Column(SMALLINT, nullable=False)
    ball_4 = Column(SMALLINT, nullable=False)
    ball_5 = Column(SMALLINT, nullable=False)
    ball_6 = Column(SMALLINT, nullable=False)
    ball_7 = Column(SMALLINT, nullable=False)

    def __init__(self, d_date, results):
        self.draw_date = d_date
        self.ball_1, self.ball_2, self.ball_3, self.ball_4, self.ball_5, \
            self.ball_6, self.ball_7 = \
            [int(results[i]) for i in range(7)]


class DrawStats(Base):
    __tablename__ = 'draw_stats'
    id = Column(db.INT, primary_key=True)
    repeated_nums = Column(db.VARCHAR(255), default=0)
    repeated_balls = Column(db.VARCHAR(255), default=0)
    frequented_nums = Column(db.VARCHAR(255), default=0)
    missing_nums = Column(db.VARCHAR(255), default=0)
    freq_and_missing = Column(db.VARCHAR(255), default=0)


class StatsTracker(Base):
    __tablename__ = 'stats_tracker'
    id = Column(db.INT, primary_key=True)
    stats_table = Column(db.VARCHAR(255), default=0)
    draw_processed = Column(db.INT, default=0)

    def __init__(self, stats_table_name, draw_id_processed):
        self.stats_table = stats_table_name
        self.draw_processed = draw_id_processed


class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(db.INT, primary_key=True)
    ticket = Column(db.VARCHAR(255), default=0)
    numbers_pool = Column(db.VARCHAR(255), default=0)
    target_date = Column(db.DATE, nullable=False)
    predicted_nums = Column(db.VARCHAR(255), default=0)
    predicted_posts = Column(db.VARCHAR(255), default=0)


class Subsequence(Base):
    __tablename__ = 'subsequence'
    id = Column(db.INT, primary_key=True)
    ball_num = Column(SMALLINT, nullable=False)
    base_num = Column(SMALLINT, nullable=False)
    subseq_num = Column(SMALLINT, nullable=False)
    frequency = Column(SMALLINT, default=0)

    def __init__(self, ball_num, base_num, subseq_num, frequency):
        self.ball_num = ball_num
        self.base_num = base_num
        self.subseq_num = subseq_num
        self.frequency = frequency


class Frequency(Base):
    __tablename__ = 'frequency'

    num = Column(db.INT, primary_key=True)
    day = Column(SMALLINT, default=0)
    date = Column(SMALLINT, default=0)
    month = Column(SMALLINT, default=0)

    def __init__(self, num, day, date, month):
        self.num = num
        self.day = day
        self.date = date
        self.month = month


class Repetition(Base):
    __tablename__ = 'repetition'

    id = Column(db.INT, primary_key=True)
    draw_date = Column(db.DATE, nullable=False)
    repeated_nums = Column(db.VARCHAR(255))
    repeated_balls = Column(db.VARCHAR(255))
    total_repeated = Column(SMALLINT, default=0)

    def __init__(self, draw_id, d_date, repeated_nums, repeated_balls, total_repeated):
        self.id = draw_id
        self.draw_date = d_date
        self.repeated_nums = repeated_nums
        self.repeated_balls = repeated_balls
        self.total_repeated = total_repeated


class FreqAndMissing(Base):
    __tablename__ = 'freq_and_missn'

    id = Column(db.INT, primary_key=True)
    draw_date = Column(db.DATE, nullable=False)
    frequented_nums = Column(db.VARCHAR(255))
    missing_nums = Column(db.VARCHAR(255))
    freq_and_missing = Column(db.VARCHAR(255))

    def __init__(self, draw_id, d_date, frequented_nums, missing_nums, freq_and_missing):
        self.id = draw_id
        self.draw_date = d_date
        self.frequented_nums = frequented_nums
        self.missing_nums = missing_nums
        self.freq_and_missing = freq_and_missing

# ============================================


class FreqByBall(Base):
    __tablename__ = 'freq_by_ball'

    drawn_number = Column(db.INT, primary_key=True)
    ball_1 = Column(SMALLINT, default=0)
    ball_2 = Column(SMALLINT, default=0)
    ball_3 = Column(SMALLINT, default=0)
    ball_4 = Column(SMALLINT, default=0)
    ball_5 = Column(SMALLINT, default=0)
    ball_6 = Column(SMALLINT, default=0)
    ball_7 = Column(SMALLINT, default=0)

    def __init__(self, drawn_number):
        self.drawn_number = drawn_number
        self.ball_number = 0


class FreqByDay(Base):
    __tablename__ = 'freq_by_day'

    drawn_number = Column(db.INT, primary_key=True)
    wed = Column(SMALLINT, default=0)
    sat = Column(SMALLINT, default=0)

    def __init__(self, drawn_number, wed, sat):
        self.drawn_number = drawn_number
        self.wed = wed
        self.sat = sat


class FreqByDate(Base):
    __tablename__ = 'freq_by_date'

    drawn_number = Column(db.INT, primary_key=True)
    date_1 = Column(SMALLINT, default=0)
    date_2 = Column(SMALLINT, default=0)
    date_3 = Column(SMALLINT, default=0)
    date_4 = Column(SMALLINT, default=0)
    date_5 = Column(SMALLINT, default=0)
    date_6 = Column(SMALLINT, default=0)
    date_7 = Column(SMALLINT, default=0)
    date_8 = Column(SMALLINT, default=0)
    date_9 = Column(SMALLINT, default=0)
    date_10 = Column(SMALLINT, default=0)
    date_11 = Column(SMALLINT, default=0)
    date_12 = Column(SMALLINT, default=0)
    date_13 = Column(SMALLINT, default=0)
    date_14 = Column(SMALLINT, default=0)
    date_15 = Column(SMALLINT, default=0)
    date_16 = Column(SMALLINT, default=0)
    date_17 = Column(SMALLINT, default=0)
    date_18 = Column(SMALLINT, default=0)
    date_19 = Column(SMALLINT, default=0)
    date_20 = Column(SMALLINT, default=0)
    date_21 = Column(SMALLINT, default=0)
    date_22 = Column(SMALLINT, default=0)
    date_23 = Column(SMALLINT, default=0)
    date_24 = Column(SMALLINT, default=0)
    date_25 = Column(SMALLINT, default=0)
    date_26 = Column(SMALLINT, default=0)
    date_27 = Column(SMALLINT, default=0)
    date_28 = Column(SMALLINT, default=0)
    date_29 = Column(SMALLINT, default=0)
    date_30 = Column(SMALLINT, default=0)
    date_31 = Column(SMALLINT, default=0)

    def __init__(self, drawn_number):
        self.drawn_number = drawn_number
        self.date_1 = 0


class FreqByMonth(Base):
    __tablename__ = 'freq_by_month'

    drawn_number = Column(db.INT, primary_key=True)
    jan = Column(SMALLINT, default=0)
    feb = Column(SMALLINT, default=0)
    mar = Column(SMALLINT, default=0)
    apr = Column(SMALLINT, default=0)
    may = Column(SMALLINT, default=0)
    jun = Column(SMALLINT, default=0)
    jul = Column(SMALLINT, default=0)
    aug = Column(SMALLINT, default=0)
    sep = Column(SMALLINT, default=0)
    oct = Column(SMALLINT, default=0)
    nov = Column(SMALLINT, default=0)
    dec = Column(SMALLINT, default=0)

    def __init__(self, drawn_number, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec):
        self.drawn_number = drawn_number
        self.jan = 0
        self.feb = 0
        self.mar = 0
        self.apr = 0
        self.may = 0
        self.jun = 0
        self.jul = 0
        self.aug = 0
        self.sep = 0
        self.oct = 0
        self.nov = 0
        self.dec = 0

