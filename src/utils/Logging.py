import logging
import json

class Logging:
    def __init__(self, log_file="logs/application.log", log_level=logging.DEBUG):
        self.setup_logger(log_file, log_level)

    def setup_logger(self, log_file, log_level):
        """Configures the logger with structured logging (JSON format)."""
        logging.basicConfig(filename=log_file, level=log_level, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_message(self, level, message, **kwargs):
        """Logs a structured JSON message."""
        log_entry = {
            "message": message,
            **kwargs
        }
        if level == 'debug':
            logging.debug(json.dumps(log_entry))
        elif level == 'info':
            logging.info(json.dumps(log_entry))
        elif level == 'warning':
            logging.warning(json.dumps(log_entry))
        elif level == 'error':
            logging.error(json.dumps(log_entry))
        else:
            logging.critical(json.dumps(log_entry))

if __name__ == "__main__":
    logger = Logging(log_level=logging.INFO)
    logger.log_message("info", "Vulnerability scan started", target="192.168.1.1", scan_type="full")
