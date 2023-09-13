"""
DBBackupService - service class to handle backing up data from DB.
"""

from src.services.dba.db_export_data import DBExportData


class DBBackupService:
    def __init__(self, db_connect):
        print("in 9 - DB Backup Service")
        # Exporting 'draw_results' table only
        data_exporter = DBExportData(db_connect, "draw_results")
        data_exporter.export_data_from_table()

        # TODO: Exporting others tables (predictions_history, etc)