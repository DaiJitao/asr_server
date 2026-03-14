import os
from loguru import logger
from pathlib import Path
import sys

from app.core.config import settings


def setup_logger():
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        log_dir / "asr_service_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        format=log_format,
        level=settings.LOG_LEVEL,
        encoding="utf-8"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True
    )

    return logger


log = setup_logger()