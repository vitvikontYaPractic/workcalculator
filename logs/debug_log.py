from loguru import logger

logger.add(
    "logs/debug.json",
    format="{time}{level}{message}",
    level="DEBUG",
    rotation="400 KB",
    compression="zip",
    serialize=True
)
