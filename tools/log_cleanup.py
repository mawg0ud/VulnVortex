import os
import time

class LogCleanup:
    def __init__(self, log_dir="logs/", retention_period=30):
        self.log_dir = log_dir
        self.retention_period = retention_period * 86400  # days to seconds

    def cleanup_logs(self):
        """Deletes logs older than the retention period."""
        current_time = time.time()
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > self.retention_period:
                    print(f"Deleting old log: {filename}")
                    os.remove(file_path)

if __name__ == "__main__":
    cleaner = LogCleanup(retention_period=30)
    cleaner.cleanup_logs()
