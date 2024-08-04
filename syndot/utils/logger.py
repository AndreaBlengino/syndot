import logging
from syndot.init_config import LOG_FILE_PATH


def log_error(error_message: str) -> None:
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.ERROR,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    logger.error(error_message)
