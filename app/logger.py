import logging

from app.config import settings

logger = logging.getLogger()
file_log = logging.FileHandler("../logs/log.txt")
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out))

logger.setLevel(settings.LOG_LEVEL)
