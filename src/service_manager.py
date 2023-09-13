"""
Manages services - reroute task manager to perform specific task to corresponding service provider
"""
from src.services.dba.db_model import FreqByBall, FreqByDay, FreqByDate, FreqByMonth
from src.services.file_status_service import FileStatusService
from src.services.dba.db_connect import DbConnect
from src.services.db_status_service import DBStatusService
from src.services.import_data_service import ImportDataService
from src.services.basic_stats_service import BasicStatsService
from src.services.basic_report_service import BasicReportService
from src.services.ticket_service import TicketService
from src.services.advanced_stats_service import AdvancedStatsService
from src.services.full_report_service import FullReportService
from src.services.db_backup_service import DBBackupService
from src.services.db_restore_service import DBRestoreService
import src.utils as utils
from src.services.dba.db_queries import BasicQueries
from src.services.tickets.wheels import Wheel
from src.services.tickets.content_generator import Contents
from src.services.analysis.repetitions import Repetitions



class ServiceManager:

    def __init__(self):
        self.service = None
        self.db_connect = DbConnect()
        self.basic_queries = BasicQueries(self.db_connect)
        self.db_last_draw_id = self.basic_queries.get_id_from_last_draw()
        self.db_last_draw_date, self.last_draw_numbers = (
            self.basic_queries.get_draw_date_numbers_by_id(self.db_last_draw_id))
        self.expected_draw_date = utils.get_expected_draw_date().date()
        self.db_status_service = None
        self.is_db_up_to_date = False
        self.file_status_service = None
        self.is_file_up_to_date = False
        self.import_data_service = None
        self.export_data_service = None
        self.restore_service = None
        self.stats_service = None

    def get_service_name(self, task_name):

        # is DB up-to-date?
        if task_name == "DB Status":
            self.process_service_db_status(self.db_last_draw_id)
            print(f"Expected (Latest) Draw: {self.expected_draw_date}")

        # is file up-to-date?
        elif task_name == "File Status":
            self.process_service_db_status(self.db_last_draw_id)
            self.process_service_file_status()

        # import latest draw into DB
        elif task_name == "Import Latest Draw":
            self.process_service_db_status(self.db_last_draw_id)
            print("DB STATUS:", self.db_status_service.is_db_up_to_date)
            self.process_service_file_status()
            print(self.is_file_up_to_date)
            self.process_service_import_latest_draws()

        # build basic stats for all draws (including latest)
        elif task_name == "Build Basic Stats":
            self.stats_service = BasicStatsService(self.db_connect)
            self.build_and_update_stats()

        # update Prediction tracker (expected vs actual)
        elif task_name == "Analyze Latest Draw":
            self.analysis_service = Repetitions(self.db_connect)

        # create report with basic stats
        elif task_name == "Generate Basic Report":
            # build basic stats for NEXT DRAW (specific month, etc)
            self.service = BasicReportService(self.db_connect)

            collected_stats = self.service.process_all_stats()
            wheel_from_basic_stats = Wheel(self.db_connect, collected_stats)
            content_generator = Contents(self.service, collected_stats, wheel_from_basic_stats)
            # content_generator.
        elif task_name == "Generate Tickets":
            self.service = TicketService()
        elif task_name == "Build Advanced Stats":
            self.service = AdvancedStatsService()
        elif task_name == "Generate HTML Report":
            self.service = FullReportService()
        elif task_name == "DB Backup":
            self.export_data_service = DBBackupService(self.db_connect)
        elif task_name == "DB Restore":
            # -- dropping and recreating tables
            self.restore_service = DBRestoreService(self.db_connect)
            self.restore_service.drop_tables()
            self.restore_service.create_tables()
            # -- optionally: delete records from draw_results table
            # self.restore_service.delete_rows("DrawResults")
            # -- importing bulk data
            self.import_data_service = ImportDataService(self.db_connect, 'bulk_draws')
            self.import_data_service.import_data_into_db()
        elif task_name == "ADDITIONAL TABLES":
            # -- dropping and recreating tables
            self.restore_service = DBRestoreService(self.db_connect)
            self.restore_service.create_tables_new()
            # -- optionally: setup tables with 70 rows to hold frequency data
            list_of_table_classes = [FreqByBall, FreqByDay, FreqByDate, FreqByMonth]
            for table_class in list_of_table_classes:
                self.restore_service.setup_table_with_49rows(table_class)
        else:
            self.service = None

    def process_service_db_status(self, last_id):
        self.db_status_service = DBStatusService(self.db_connect, self.expected_draw_date)

        self.db_status_service.get_latest_record_in_db(last_id)
        self.db_last_draw_date = self.db_status_service.last_draw_date_in_db
        self.db_status_service.get_db_status()
        self.is_db_up_to_date = self.db_status_service.is_db_up_to_date

    def process_service_file_status(self):
        self.file_status_service = FileStatusService(self.expected_draw_date, self.db_last_draw_date)
        self.file_status_service.get_file_status()
        self.is_file_up_to_date = self.file_status_service.is_file_up_to_date

    def process_service_import_latest_draws(self):
        if self.is_file_up_to_date:
            if not self.is_db_up_to_date:
                self.import_data_service = ImportDataService(self.db_connect, 'latest_draws')
                self.import_data_service.import_data_into_db()
                self.import_data_service.delete_duplicates()
            else:
                print("DB is up-to-date, nothing to do here")
        else:
            print("[WARNING] File is NOT up-to-date, aborting request to import data")

    def build_and_update_stats(self):
        self.process_repetition()
        self.process_freq_and_missing()
        self.process_basic_stats()
        self.process_subsequence()

    def process_repetition(self):
        last_id_processed_repetition = self.basic_queries.get_last_processed_id_from_stats_tracker('repetition')
        if last_id_processed_repetition == self.db_last_draw_id:
            print('INFO: repetition already up to date in DB')
        else:
            self.stats_service.build_repetition_stats()
            self.stats_service.update_repetition_stats()

    def process_freq_and_missing(self):
        last_id_processed_freq_and_missn = self.basic_queries.get_last_processed_id_from_stats_tracker('freq_and_missn')
        if last_id_processed_freq_and_missn == self.db_last_draw_id:
            print('INFO: freq_and_missing_stats already up to date in DB')
        else:
            self.stats_service.build_freq_and_missing_stats()
            self.stats_service.update_freq_and_missing_stats()

    def process_basic_stats(self):
        stats_to_skip = []
        last_id_processed_freq_by_ball = self.basic_queries.get_last_processed_id_from_stats_tracker('freq_by_ball')
        if last_id_processed_freq_by_ball == self.db_last_draw_id:
            print('INFO: freq_by_ball already up to date in DB')
            stats_to_skip.append('freq_by_ball')

        last_id_processed_freq_by_month = self.basic_queries.get_last_processed_id_from_stats_tracker('freq_by_month')
        if last_id_processed_freq_by_month == self.db_last_draw_id:
            print('INFO: freq_by_month already up to date in DB')
            stats_to_skip.append('freq_by_month')

        last_id_processed_freq_by_day = self.basic_queries.get_last_processed_id_from_stats_tracker('freq_by_day')
        if last_id_processed_freq_by_day == self.db_last_draw_id:
            print('INFO: freq_by_day already up to date in DB')
            stats_to_skip.append('freq_by_day')
            
        last_id_processed_freq_by_date = self.basic_queries.get_last_processed_id_from_stats_tracker('freq_by_date')
        if last_id_processed_freq_by_date == self.db_last_draw_id:
            print('INFO: freq_by_date already up to date in DB')
            stats_to_skip.append('freq_by_date')

        self.stats_service.build_basic_stats(stats_to_skip)
        self.stats_service.update_basic_stats(stats_to_skip)

    def process_subsequence(self):
        last_id_processed_subsequence = self.basic_queries.get_last_processed_id_from_stats_tracker('subsequence')
        if last_id_processed_subsequence == self.db_last_draw_id:
            print('INFO: subsequence already up to date in DB')
        else:
            self.stats_service.build_subsequence_stats()
            self.stats_service.update_subsequence_stats()
