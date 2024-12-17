import logging
from datetime import datetime
import os
from colorama import Fore, Style

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('HydraMarketplace')
        self._setup_logger()

    def _setup_logger(self):
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            
            # Create logs directory if it doesn't exist
            os.makedirs('logs', exist_ok=True)
            
            # File handler
            fh = logging.FileHandler(f'logs/hydra_{datetime.now().strftime("%Y%m%d")}.log')
            fh.setLevel(logging.INFO)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def info(self, message, color=Fore.YELLOW):
        formatted_message = f"{color}{message}{Style.RESET_ALL}"
        self.logger.info(formatted_message)
        print(formatted_message)

    def error(self, message):
        formatted_message = f"{Fore.RED}{message}{Style.RESET_ALL}"
        self.logger.error(formatted_message)
        print(formatted_message)

    def warning(self, message):
        formatted_message = f"{Fore.YELLOW}{message}{Style.RESET_ALL}"
        self.logger.warning(formatted_message)
        print(formatted_message)

    def success(self, message):
        formatted_message = f"{Fore.GREEN}{message}{Style.RESET_ALL}"
        self.logger.info(formatted_message)
        print(formatted_message)

# Create a global logger instance
logger = Logger()

def log_message(message, color=Fore.YELLOW):
    """
    Compatibility function for existing code that uses log_message directly
    """
    logger.info(message, color)