import os
import logging
from src.config.settings import settings


def setup_logger() -> logging.Logger:
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    log_filepath = os.path.join(settings.OUTPUT_DIR, "execution.log")

    logger = logging.getLogger("BrowserStack_CE_Pipeline")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(
            log_filepath, mode="a", encoding="utf-8"
        )
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(threadName)s: %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
