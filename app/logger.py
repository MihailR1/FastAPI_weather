import logging

from app.config import settings

logger = logging.getLogger()
file_log = logging.FileHandler(settings.LOG_FILES_PATH)
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out))

logger.setLevel(settings.LOG_LEVEL)
