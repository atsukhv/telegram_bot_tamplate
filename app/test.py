import logging
import colorlog
from loguru import logger

# Создаем логгер
loggerr = colorlog.getLogger("example_logger")

# Устанавливаем уровень логирования
loggerr.setLevel(logging.DEBUG)

# Создаем обработчик с цветным форматированием
handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s%(reset)s",
    datefmt=None,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

handler.setFormatter(formatter)
loggerr.addHandler(handler)

# Примеры логирования
loggerr.debug("Это отладочное сообщение")
loggerr.info("Это информационное сообщение")
loggerr.warning("Это предупреждение")
loggerr.error("Это сообщение об ошибке")
loggerr.critical("Это критическое сообщение")
print('')
logger.info("Это информационное сообщение")
logger.debug("Это отладочное сообщение")
logger.error("Это сообщение об ошибке")
logger.warning("Это предупреждение")
logger.critical("Это критическое сообщение")
logger.success("Это успех")
logger.trace('Это трассировка')
