import logging
from aiologger.colorize import ColoredFormatter

# Настройка логирования
alogger = logging.getLogger("alogger")
alogger.setLevel(logging.DEBUG)

# Создание консольного обработчика
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Добавление обработчика к логгеру
alogger.addHandler(console_handler)

async def date_and_time_format(show_time=True, show_date=True):
    """
    Форматирует дату и время в соответствии с настройками
    """
    formatter = ColoredFormatter(show_time=show_time, show_date=show_date)
    console_handler.setFormatter(formatter)  # Устанавливаем форматтер для обработчика
