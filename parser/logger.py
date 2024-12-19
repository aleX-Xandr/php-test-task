import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record) -> None:
        """
        Find caller from where originated the logged message
        """
        level = logger.level(record.levelname).name
        frame, depth = logging.currentframe(), 2
        frame_back = frame.f_back
        while frame.f_code.co_filename == logging.__file__:
            frame = frame_back or frame
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging() -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
