import os
import logging
from datetime import datetime, timedelta
from typing import List

class LogCleanup:
    """
    A utility class to manage and clean up log files.

    Features:
    - Automatically deletes logs older than a defined retention period.
    - Compresses old logs to save disk space.
    - Generates cleanup reports for auditing purposes.
    - Configurable via parameters for directories, retention policies, and compression settings.
    """

    def __init__(self, log_directory: str, retention_days: int = 30, compression: bool = True):
        """
        Initializes the LogCleanup utility.

        Args:
            log_directory (str): Path to the directory containing log files.
            retention_days (int): Number of days to retain log files.
            compression (bool): Whether to compress logs older than the retention period.
        """
        self.log_directory = log_directory
        self.retention_days = retention_days
        self.compression = compression
        self.logger = logging.getLogger("LogCleanup")
        self.logger.setLevel(logging.INFO)

        if not os.path.exists(self.log_directory):
            raise ValueError(f"Log directory does not exist: {self.log_directory}")

    def clean_logs(self):
        """
        Perform the log cleanup process.
        """
        self.logger.info(f"Starting log cleanup in directory: {self.log_directory}")
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        cleanup_summary = {
            "deleted": [],
            "compressed": [],
        }

        for log_file in self._get_log_files():
            file_path = os.path.join(self.log_directory, log_file)
            file_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))

            if file_modified_date < cutoff_date:
                if self.compression:
                    self._compress_file(file_path, cleanup_summary)
                else:
                    self._delete_file(file_path, cleanup_summary)

        self._generate_cleanup_report(cleanup_summary)
        self.logger.info("Log cleanup completed.")

    def _get_log_files(self) -> List[str]:
        """
        Retrieve all log files in the specified directory.

        Returns:
            List[str]: List of log filenames.
        """
        self.logger.debug("Fetching log files from directory.")
        return [
            f for f in os.listdir(self.log_directory)
            if os.path.isfile(os.path.join(self.log_directory, f)) and f.endswith(".log")
        ]

    def _delete_file(self, file_path: str, summary: dict):
        """
        Delete a log file and update the cleanup summary.

        Args:
            file_path (str): Path to the log file to delete.
            summary (dict): Dictionary to store cleanup results.
        """
        try:
            os.remove(file_path)
            self.logger.info(f"Deleted log file: {file_path}")
            summary["deleted"].append(file_path)
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {e}")

    def _compress_file(self, file_path: str, summary: dict):
        """
        Compress a log file to save disk space.

        Args:
            file_path (str): Path to the log file to compress.
            summary (dict): Dictionary to store cleanup results.
        """
        try:
            import gzip
            compressed_file = f"{file_path}.gz"

            with open(file_path, 'rb') as f_in, gzip.open(compressed_file, 'wb') as f_out:
                f_out.writelines(f_in)

            os.remove(file_path)
            self.logger.info(f"Compressed log file: {file_path} -> {compressed_file}")
            summary["compressed"].append(compressed_file)
        except Exception as e:
            self.logger.error(f"Failed to compress file {file_path}: {e}")

    def _generate_cleanup_report(self, summary: dict):
        """
        Generate a report summarizing the cleanup process.

        Args:
            summary (dict): Dictionary containing cleanup results.
        """
        report_path = os.path.join(self.log_directory, "cleanup_report.txt")
        try:
            with open(report_path, 'w') as report:
                report.write("Log Cleanup Report\n")
                report.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                report.write(f"Deleted Files ({len(summary['deleted'])}):\n")
                for file in summary["deleted"]:
                    report.write(f"  - {file}\n")
                report.write(f"\nCompressed Files ({len(summary['compressed'])}):\n")
                for file in summary["compressed"]:
                    report.write(f"  - {file}\n")

            self.logger.info(f"Cleanup report generated at: {report_path}")
        except Exception as e:
            self.logger.error(f"Failed to generate cleanup report: {e}")


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Parameters for the cleanup utility
    log_dir = "./logs"
    retention = 7
    enable_compression = True

    log_cleanup = LogCleanup(log_directory=log_dir, retention_days=retention, compression=enable_compression)
    log_cleanup.clean_logs()
