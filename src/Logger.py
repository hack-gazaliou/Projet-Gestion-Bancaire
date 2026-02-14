import logging
import sys

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.WARNING,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
)
logger = logging.getLogger(__name__)
logger.debug("Logger Ready !")
