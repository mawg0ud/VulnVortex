import logging
import os

class ErrorHandler:
    def __init__(self, log_file="logs/errors.log"):
        self.setup_logger(log_file)

    def setup_logger(self, log_file):
        """Configures the error logging."""
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(filename=log_file, level=logging.ERROR, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_error(self, message):
        """Logs an error message."""
        logging.error(message)

    def handle_exception(self, ex):
        """Logs an exception."""
        logging.exception(f"Exception occurred: {ex}")

if __name__ == "__main__":
    error_handler = ErrorHandler()
    try:
        # Example use
        1 / 0
    except Exception as e:
        error_handler.handle_exception(e)
