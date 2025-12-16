import sys
import tomllib
from pathlib import Path

from loguru import logger

path_to_config = Path("config.toml").absolute()


def get_env_type():
    with open(path_to_config, "rb") as f:
        data = tomllib.load(f)
    return data['env']['env_type']


def setup_logging():
    """
    Настраивает логгер для всего приложения в зависимости от окружения.
    """
    # Удаляем стандартный обработчик, чтобы избежать дублирования
    logger.remove()

    # Определяем формат для консоли (разработка)
    dev_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )

    # Определяем формат для файла (продакшен)
    prod_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    # Конфигурация для разработки (если не указано иное)
    if get_env_type() == "debug":
        logger.add(sys.stderr, level="DEBUG", format=dev_format, colorize=True)
        logger.info("Режим разработки: логирование настроено для вывода в консоль.")

    # Конфигурация для продакшена
    else:
        # В консоль выводим только важные сообщения
        logger.add(sys.stderr, level="INFO", format=prod_format, colorize=False)

        # В файл пишем все, начиная с DEBUG, в формате JSON для машинного анализа
        logger.add(
            "logs/app.log",
            level="DEBUG",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            serialize=True,  # Структурированное логирование в JSON
        )
        logger.info("Режим продакшена: логирование настроено для вывода в консоль и файл.")
