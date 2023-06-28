import logging
import sys

from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """Класс для перехвата логов для loguru."""

    def emit(self, record):
        # Получаем соответствущий уровень логов
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Проверяем, откуда получено сообщение
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    logging.basicConfig(handlers=[InterceptHandler()], level=settings.log_level)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    logger.remove()
    logger.add(sys.stdout, level='INFO')
    logger.add(
        settings.log_location,
        rotation=settings.log_rotation_time,
        compression=settings.log_compression,
        level=settings.log_level,
    )
