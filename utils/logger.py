import logging
import os

# --> create logs folder
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("Annonces_logger")
logger.setLevel(logging.INFO)

# --> formatter
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# --> file handler 
file_handler = logging.FileHandler("logs/scraping.log")
file_handler.setFormatter(formatter)

# --> console handler (docker)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# --> add handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# --> functions
def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)
