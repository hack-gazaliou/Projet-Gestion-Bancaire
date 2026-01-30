import logging

logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        filename='bank.log',
        level= logging.INFO
    )
logger = logging.getLogger(__name__)
logger.debug("Logger Ready !")