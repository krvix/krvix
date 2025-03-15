import logging
import sys
from datetime import datetime
import os
from logging.handlers import RotatingFileHandler
from src.config.settings import LOG_LEVEL, LOG_FORMAT


class Logger:
    def __init__(self, name: str, log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

        # Create formatter
        formatter = logging.Formatter(LOG_FORMAT)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create file handler if log file is specified
        if log_file:
            log_dir = os.path.dirname(log_file)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = RotatingFileHandler(
                log_file, maxBytes=10485760, backupCount=5  # 10MB
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        self.logger.info(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs):
        self.logger.error(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs):
        self.logger.warning(self._format_message(message, **kwargs))

    def debug(self, message: str, **kwargs):
        self.logger.debug(self._format_message(message, **kwargs))

    def _format_message(self, message: str, **kwargs) -> str:
        if kwargs:
            message = f"{message} | Additional Info: {kwargs}"
        return message


class BlockchainLogger(Logger):
    def __init__(self):
        super().__init__("blockchain", "logs/blockchain.log")

    def log_transaction(self, tx_hash: str, status: str, **kwargs):
        self.info(f"Transaction: {tx_hash} | Status: {status}", **kwargs)


class AILogger(Logger):
    def __init__(self):
        super().__init__("ai", "logs/ai.log")

    def log_prediction(self, model_name: str, accuracy: float, **kwargs):
        self.info(f"Model: {model_name} | Accuracy: {accuracy:.4f}", **kwargs)


class APILogger(Logger):
    def __init__(self):
        super().__init__("api", "logs/api.log")

    def log_request(self, method: str, endpoint: str, status_code: int, **kwargs):
        self.info(
            f"Method: {method} | Endpoint: {endpoint} | Status: {status_code}", **kwargs
        )


# Create logger instances
blockchain_logger = BlockchainLogger()
ai_logger = AILogger()
api_logger = APILogger()
