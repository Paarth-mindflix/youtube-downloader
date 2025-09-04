import logging
import os
import sys
from colorama import Fore, Style, init


class CustomLogger:
    def __init__(self, log_file_path, level=logging.DEBUG):
        """
        Initializes the CustomLogger instance.

        :param log_file_path: Path to the log file.
        :param level: Logging level (default: logging.DEBUG).
        """
        # Initialize colorama for cross-platform color support
        init(autoreset=True)

        # Create the log directory if it does not exist
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        # Clear any existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Ensure stdout supports UTF-8
        sys.stdout.reconfigure(encoding='utf-8')

        # Console handler with color support and UTF-8 encoding
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = self._get_color_formatter()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _get_color_formatter(self):
        """
        Returns a logging formatter with color support for different log levels.
        """

        class ColorFormatter(logging.Formatter):
            COLOR_MAP = {
                logging.DEBUG: Fore.BLUE + Style.BRIGHT,
                logging.INFO: Fore.GREEN + Style.BRIGHT,
                logging.WARNING: Fore.YELLOW + Style.BRIGHT,
                logging.ERROR: Fore.RED + Style.BRIGHT,
                logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
            }

            def format(self, record):
                color = self.COLOR_MAP.get(record.levelno, Style.RESET_ALL)
                record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
                record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
                return super().format(record)

        return ColorFormatter("%(asctime)s - %(levelname)s - %(message)s")

    def get_logger(self):
        """
        Returns the configured logger instance.
        """
        return self.logger