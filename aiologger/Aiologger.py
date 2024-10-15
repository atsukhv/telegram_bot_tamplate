import sys
import traceback
import logging

from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from config import BLUIXCODE_ADMIN_GROUP
from aiologger.colorize import ColoredFormatter

# Настройка логирования
logger = logging.getLogger("aiogram_logger")
logger.setLevel(logging.DEBUG)

# Создание консольного обработчика
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)



# Добавление обработчика к логгеру
logger.addHandler(console_handler)


class ErrorLoggingMiddleware(BaseMiddleware):
    def __init__(self, log_errors=True, log_messages=True, log_callbacks=True, log_handlers=True, show_time=False,
                 show_date=False):
        super().__init__()
        self.log_errors = log_errors
        self.log_messages = log_messages
        self.log_callbacks = log_callbacks
        self.log_handlers = log_handlers
        self.show_time = show_time
        self.show_date = show_date

    async def __call__(self, handler, event: Update, data: dict, message: Message | None = None):

        # Создание форматтера
        formatter = ColoredFormatter(show_time=self.show_time, show_date=self.show_date)
        console_handler.setFormatter(formatter)

        if self.log_messages and isinstance(event, Message):
            logger.info(f"Получено сообщение с ID: {event.message_id}")

        if self.log_callbacks and event.callback_query is not None:
            logger.info(f"Получен колбэк: {event.callback_query.data}")

        try:
            result = await handler(event, data)
            if self.log_handlers:
                logger.info(f"Хэндлер выполнен: {handler.__name__}")
            return result
        except Exception as e:
            if self.log_errors:
                self.log_error(e, event)
            return None

    def log_error(self, e, event):
        error_message = f'Ошибка: {str(e)}'
        logger.error(error_message)

        # Получаем информацию о строке, где произошла ошибка
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)

        if tb:
            filename, lineno, funcname, _ = tb[-1]
            error_location = f'Ошибка произошла в файле: {filename.split("\\")[-1]}, строка: {lineno}, в функции: {funcname}'
            logger.error(error_location)

        # Отправка сообщения об ошибке в админ-группу
        # if 'message' in data and data['message'] is not None:
        #     await data['message'].bot.send_message(chat_id=BLUIXCODE_ADMIN_GROUP, text
