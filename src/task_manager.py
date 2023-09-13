"""TaskManager class:
        - handles User Options
            - DB maintenance
            - Stats Generation
            - Tickets Generation
            - Reports Generation
            """


def get_options_list():
    user_options = []
    user_options.append("1 - DB Status")  # is DB up-to-date?
    user_options.append("2 - File Status")  # is file up-to-date?
    user_options.append("3 - Import Latest Draw")  # import latest draw into DB
    user_options.append("4 - Build Basic Stats")  # build basic stats for all draws (including latest)
    user_options.append("5 - Analyze Latest Draw")  # update Prediction tracker (expected vs actual)
    user_options.append("6 - Generate Basic Report")  # create report with basic stats
    user_options.append("7 - Generate Tickets")
    user_options.append("8 - Build Advanced Stats")
    user_options.append("9 - Generate HTML Report")
    user_options.append("10 - DB Backup")
    user_options.append("11 - DB Restore")
    user_options.append("12 - ADDITIONAL TABLES")
    user_options.append("q - QUIT")
    return user_options


class TaskManager:
    def __init__(self):
        self.user_options = get_options_list()
        self.task_id = None
        self.task_name = None

    def map_request_to_task(self, option_id):
        self.get_task_name(option_id)

    def get_task_name(self, option_id):
        request = int(option_id)
        if request in range(1, 13):
            task_name_with_id = self.user_options[request - 1]
            self.task_id = task_name_with_id.split('-')[0].strip()
            self.task_name = task_name_with_id.split('-')[1].strip()
        else:
            self.task_id = 12
            self.task_name = "QUIT"
