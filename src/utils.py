import json
import platform
from os import path
from datetime import datetime, timedelta

from sqlalchemy import inspect

def get_home_dir():
    current_os = platform.system()
    HOME_DIR = "/home/praba"
    if current_os == 'Linux':
        HOME_DIR = "/home/praba"
    elif current_os == 'Darwin':
        HOME_DIR = "/Users/praba"
    return HOME_DIR


def file_exists(filename):
    return path.exists(filename)


def sql_result_to_list(results):
    result_list = [list(row) for row in results]
    return result_list


def to_list_from_str(string_in):
    list_out = []
    list_out_org = str(string_in).split(',')
    for item in list_out_org:
        list_out.append(int(item.strip()))
    return list_out


def to_list_from_dict(dict_in):
    list_out = []
    for item in dict_in:
        list_out.append(item)
    return list_out


def to_str_from_list(list_in, join_by=', '):
    string_ints = [str(int) for int in list_in]
    return join_by.join(string_ints)


def string_to_date(str_date):
    datetime_obj = datetime.strptime(str_date, '%d-%B-%Y')
    return datetime_obj.date()


def string_to_time(str_time):
    time_obj = datetime.strptime(str_time, '%H:%M:%S')
    return time_obj.time()

def time_to_string(time_str):
    time_string = datetime.strftime(time_str, '%H:%M:%S')
    return time_string

def date_to_string(date_obj):
    return date_obj.strftime("%Y %B %d, %A")
def get_hour_of_timestamp(time_obj):
    # time_obj = datetime.strftime(time_string, '%H:%M:%S')
    return time_obj.hour

def get_today_date(string=False):
    # Textual month, day and year
    today = datetime.now()
    if string:
        return today.strftime("%Y %B %d, %A : %I:%M:%p")
    return today

def get_yesterday(string=False):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime('%Y-%B-%d')
    return yesterday


def get_day_of_week(date_in):
    # return calendar.day_name[date_in.weekday()]
    # return date_in.strftime('%b') # abreviated/short
    return date_in.strftime('%a').lower()
def get_date_of_month(date_in):
    return date_in.strftime('%-d')

def get_month_of_year(date_in):
    # month_abre = date_in.strftime('%b')
    return date_in.strftime('%b').lower()


def get_time_delta(hours_diff, date_in=None):
    if date_in is None:
        return str(datetime.now() + timedelta(hours=hours_diff))
    else:
        print("PLEASE implement")

def get_date_of_last_wednesday():
    today = datetime.now()
    offset = (today.weekday() - 2) % 7
    last_wednesday = today - timedelta(days=offset)
    return last_wednesday

def get_date_of_last_saturday():
    today = datetime.now()
    offset = (today.weekday() - 5) % 7
    last_saturday = today - timedelta(days=offset)
    return last_saturday

def is_date2_latest(date1, date2):
    # from datetime import date, timedelta

    # Create two date objects
    # date1 = date(2021, 5, 10)
    # date2 = date(2021, 5, 15)

    # Calculate the difference between the two dates
    is_date2_latest = False
    delta = date2 - date1

    # Compare the difference in days
    if delta.days > 0:
        is_date2_latest = True
    elif delta.days < 0:
        is_date2_latest = False
    else:
        is_date2_latest = True # equal
    return is_date2_latest

def get_expected_draw_date():
    current_date = get_today_date().date()
    # print("CURRENT DATE: " + current_timestamp.strftime("%A %B %d, %Y"))
    expected_draw_date = ''
    date_of_last_saturday = get_date_of_last_saturday()
    date_of_last_wednesday = get_date_of_last_wednesday()
    saturday_later_than_wednesday = is_date2_latest(date_of_last_wednesday, date_of_last_saturday)
    if saturday_later_than_wednesday:
        expected_draw_date = date_of_last_saturday
    else:
        expected_draw_date = date_of_last_wednesday

    return expected_draw_date


def get_future_draw_date():
    """NEED:
        dateOfMonth = date_1,..., date_31
        month = jan,..., dec
        day = mon,..., sun
    """
    current_timestamp = get_today_date()
    # print("CURRENT TIMESTAMP: " + current_timestamp.strftime("%A %B %d, %Y %I:%M:%p"))
    #
    # [datetime.datetime(2023, 9, 4, 5, 22, 5, 184840), 'September', '04', 'Monday', 5, 'AM']
    current_timestamp = get_today_date(False)

    month = get_month_of_year(current_timestamp)
    dateofmonth = get_date_of_month(current_timestamp)
    day = get_day_of_week(current_timestamp)

    next_draw_timestamp = [current_timestamp, month, dateofmonth, day]
    return next_draw_timestamp

# ========= Dictionary utils =================================


def dict_to_json_object(sorted_dict):
    json_object = json.dumps(sorted_dict, indent=4)
    # print(json_object)
    return json_object


def object_to_dict(obj):
    # -- convert objects from sqlalchemy query results to dict
    # -- object ===> into  dict {}
    # def parse_result_into_dict(self, query_result):
    #     rows_dict = [dict(row) for row in query_result.fetchall()]
    #     return rows_dict
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def create_dict_of_balls():
    # dictionary of balls from 1 to 20
    ball_dict = {}
    for num in range(1, 8):
        ball_dict[num] = create_dict_of_base_numbers()
    return ball_dict

def create_dict_of_base_numbers():
    # dictionary of base numbers from 1 to 70
    base_number_dict = {}
    for num in range(1, 50):
        # if num in range(1, 10):
        #     num = "0" + str(num)
        base_number_dict[num] = create_dict_of_subseq_numbers()
    return base_number_dict

def create_dict_of_subseq_numbers():
    # dictionary of subseq numbers from 1 to 70
    subseq_number_dict = {}
    for num in range(1, 50):
        # if num in range(1, 10):
        #     num = "0" + str(num)
        subseq_number_dict[num] = 0
    return subseq_number_dict

def create_dict_of_months():
    # dictionary of months from 1 to 12
    months = ['jan', 'feb','mar', 'apr','may', 'jun', 'jul', 'aug','sep', 'oct', 'nov', 'dec']
    month_dict = {}
    for num in range(0, 12):
        month_dict[months[num]] = 0
    return month_dict

def create_dict_of_days_of_week():
    # dictionary of weekdays from 1 to 7
    days = ['mon', 'tue', 'wed', 'thu', 'fri','sat','sun']
    day_dict = {}
    for num in range(0, 7):
        day_dict[days[num]] = 0
    return day_dict


def create_dict_of_dates_of_month():
    # dictionary of days of month from 1 to 31
    date_dict = {}
    for num in range(1, 32):
        date_dict[str(num)] = 0
    return date_dict

def get_list_of_balls():
    # create a list of balls from 1 to 20
    ball_list = []
    for num in range(1, 8):
        ball_list.append('ball_' + str(num))
    return ball_list

def convert_list_of_balls_to_string(list_of_balls):
    # convert a list of balls to a string
    string_list = ''
    for ball in list_of_balls:
        string_list = string_list + ball + ','
    if string_list[-1] == ',':
        string_list = string_list.rstrip(',')
    return string_list

def create_dict_of_draw_results():
    # dictionary of freq encloses dicts of balls, months, days of week, dates of month, times of day
    ball_dict = create_dict_of_balls()
    month_dict = create_dict_of_months()
    day_dict = create_dict_of_days_of_week()
    date_dict = create_dict_of_dates_of_month()
    base_number_dict = create_dict_of_base_numbers()
    stats = {
             'days': day_dict,
             'dates': date_dict,
             'months': month_dict,
             'balls': ball_dict
             }
    freq_dict = {}
    for key in base_number_dict.keys():
        freq_dict[key] = [stats]
    return freq_dict


# copied from archived 2022 projects, not Used yet here in 2023
def entries_to_remove(entries, base_numbers_ss_numbers):
    for key in entries:
        if key in base_numbers_ss_numbers:
            # print(f"Deleting {the_dict[key]}")
            del base_numbers_ss_numbers[key]
            for base_numbers, ss_numbers in base_numbers_ss_numbers.items():
                if key in ss_numbers:
                    del ss_numbers[key]
        # for key in entries:
        #     for base_numbers, ss_numbers in base_numbers_ss_numbers.items():
        #         if key in ss_numbers:
        #             del ss_numbers[key]
            # print(f"SS ==> {ss_numbers.values()}")

def build_ss_numbers_dict(position):
    ss_numbers_dict = {}
    # range_by_position = [(1,51), (2, 52), (3,53), (4, 54), (5,55),
    #                      (6,56), (7, 57), (8,58), (9, 59), (10,60),
    #                      (11,61), (12, 62), (13,63), (14, 64), (15,65),
    #                      (16,66), (17, 67), (18,68), (19, 69), (20,70),]
    min = int(position.split('_')[1])
    max = min + 48 # 51
    ss_numbers = ['ss_' + str(ss_num) for ss_num in range(1, 50)]
    for ss_num in ss_numbers:
        ss_numbers_dict[ss_num] = 0
    return ss_numbers_dict

def build_base_numbers_dict(position):
    base_numbers_dict = {}
    min = int(position.split('_')[1])
    max = min + 48 # 51
    base_numbers = ['b_' + str(num) for num in range(1, 50)]
    for num in base_numbers:
        base_numbers_dict[num] = build_ss_numbers_dict(position)
    return base_numbers_dict

def build_positions_dict():
    positions_dict = {}
    positions = ['p_' + str(p) for p in range(1, 8)]
    for position in positions:
        positions_dict[position] = build_base_numbers_dict(position)
    return positions_dict

def build_base_freq_dict(position):
    base_numbers_freq_dict = {}
    min = int(position.split('_')[1])
    max = min + 48 # 51
    base_numbers = ['b_' + str(num) for num in range(min, max)]
    for num in base_numbers:
        base_numbers_freq_dict[num] = 0
    return base_numbers_freq_dict

def build_freq_by_position_structure():
    positions_dict = {}
    positions = ['p_' + str(p) for p in range(1, 8)]
    for position in positions:
        positions_dict[position] = build_base_freq_dict(position)
    return positions_dict

def build_subseq_by_position_structure(position=1):
    # -- root keys are based on 20 positions
    positions = [p for p in range(1, 8)]
    # print(f"Positions: {positions}")

    # -- second level keys are based on 'POSSIBLE' numbers, for each position
    base_numbers = [num for num in range(1, 50)]

    # -- third level keys are based on 'SUBSEQUENT' numbers, for each position, AND value = Frequency
    ss_numbers = [ss_num for ss_num in range(1, 50)]

    # -- Setup Dictionary Structure
    positions_dict = build_positions_dict()

    ## ==== For each position group, remove unused/extra entries in
    # ss_numbers_dict and base_numbers_dict
    postn_keys = positions
    # to remove [0, 51, 50, 49, 48, 47 ; ]
    base_keys = [[51], [51, 50], [51, 50, 49], list(range(51, 47, -1)),
                 list(range(51, 46, -1)), list(range(51, 45, -1)), list(range(51, 44, -1)),list(range(51, 43, -1)), list(range(51, 42, -1)),
                 list(range(51, 41, -1)), list(range(51, 40, -1)), list(range(51, 39, -1)), list(range(51, 38, -1)),list(range(51, 37, -1)),
                 list(range(51, 36, -1)), list(range(51, 35, -1)), list(range(51, 34, -1)),list(range(51, 33, -1)),list(range(51, 32, -1))]


    return positions_dict

def convert_results_dict_to_list(results_dict):
    # -- create list of values from dict
    # -- dict {} ===> into  list []
    result = []
    for key, value in results_dict.items():
        if 'pos_' in key:
            result.append(value)
    return result
def loads_json_and_sort(json_object):
    # Parsing Json object
    json_parse = json.loads(json_object)

    # iterating
    for it in json_parse['Student']:
        for y in it['subject']:
            print(y['code'], y['grade'], it['enrollment_no'], it['name'])

# def generate_json_html_files(self, sorted_by_freq_dict, json_object, file_name="freq_by_pos"):
#     #--- create JSON file
#     json_file = HOME_DIR.OUTPUT_LOCATION + file_name + '.json'
#     with open(json_file, 'w') as file:
#         json.dump(sorted_by_freq_dict, file, indent=4, sort_keys=True)
#
#     #--- create HTML Table file
#     # html_top_file = DataImporter.OUTPUT_LOCATION +  file_name + '.html'
#     html_table = json2html.convert(json = json_object)
#     html_file = HOME_DIR.OUTPUT_LOCATION +  file_name + '.html'
#     # with open(html_top_file, 'r') as html_file_out:
#     #     html_file_out.writelines(html_table)
#     with open(html_file, 'w') as html_file_out:
#         html_file_out.writelines(html_table)
#
#     return html_file_out


def convert_string_to_list_of_numbers(str_to_convert):
    # input str('{4,11,27,54,56}') ==> list([4,11,27,54,56])
    str_brackets_removed = str_to_convert.replace('{', '').replace('}', '')
    list_of_string = str_brackets_removed.split(',')
    list_of_numbers = []
    for str in list_of_string:
        if str != '':
            list_of_numbers.append(int(str))
    return list_of_numbers


def create_dict_collection(numbers_list):
    collection_dict = {}
    for num in numbers_list:
        if num not in collection_dict.keys():
            collection_dict[num] = 1
        else:
            collection_dict[num] += 1
    # print(collection_dict)
    return collection_dict


def sorted_dict_by_value(unsorted_dict):
    sorted_by_freq = sorted(unsorted_dict.items(), key=lambda x: x[1], reverse=True)
    converted_dict = dict(sorted_by_freq)
    return converted_dict