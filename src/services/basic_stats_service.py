"""
BasicStatsService - service class to handle compiling basic stats.

1. Service_Manager calls Basic_stats_service asks for basic stats.
2. Basic_stats_service calls Basic_stats_collector to collect stats.
3. Basic_stats_collector calls FreqBy_Stats to process 'frequented_by_*' stats.
4. Basic_stats_collector calls RepetitionMissing_Stats to process 'repeated', 'missed' stats
5. Basic_stats_updater updates stats in DB.

"""
from src.services.basic_stats.basic_stats_collector import BasicStatsCollector
from src import utils
from src.services.basic_stats.basic_stats_updater import BasicStatsUpdater



class BasicStatsService:
    def __init__(self, db_connect):
        print("in 4- BasicStatsService")
        self.db_connect = db_connect
        self.stats_collector = BasicStatsCollector(self.db_connect)
        self.basic_stats = None
        self.repetition_stats = None
        self.freq_missing_stats = None
        self.subsequence_stats = None

    def build_basic_stats(self, stats_to_skip):
        # Get basic stats dictionary from stats collection
        self.basic_stats = self.stats_collector.build_basic_stats(stats_to_skip)

    def build_repetition_stats(self):
        self.repetition_stats = self.stats_collector.build_repetition_stats()

    def build_freq_and_missing_stats(self):
        self.freq_missing_stats = self.stats_collector.build_freq_and_missing_stats()
        # for key, value in self.freq_missing_stats.items():
        #     print(key, value)

    def build_subsequence_stats(self):
        self.subsequence_stats = self.stats_collector.build_subsequence_stats()

    def update_basic_stats(self, stats_to_skip):
        # Update DB stats tables with data from stats collection
        self.stats_collector.update_basic_stats(stats_to_skip)

    def update_repetition_stats(self):
        self.stats_collector.update_repetition_stats()

    def update_freq_and_missing_stats(self):
        self.stats_collector.update_freq_and_missing_stats()

    def update_subsequence_stats(self):
        self.stats_collector.update_subsequence_stats()

