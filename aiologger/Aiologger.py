import sys
import traceback

from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from config import BLUIXCODE_ADMIN_GROUP


from aiologger.al_settings import alogger, date_and_time_format


class ErrorLoggingMiddleware(BaseMiddleware):
    def __init__(self, log_errors=True, log_messages=True, log_callbacks=True, log_handlers=True, show_time=True,
                 show_date=True):
        super().__init__()
        self.log_errors = log_errors
        self.log_messages = log_messages
        self.log_callbacks = log_callbacks
        self.log_handlers = log_handlers
        self.show_time = show_time
        self.show_date = show_date

    async def __call__(self, handler, event: Update, data: dict, message: Message | None = None):
        await date_and_time_format(self.show_time, self.show_date) # Форматирование даты и времени

        # Логирование сообщений
        if self.log_messages and isinstance(event, Message):
            alogger.info(f"Получено сообщение с ID: {event.message_id}")

        # Логирование колбэков
        if self.log_callbacks and event.callback_query is not None:
            alogger.info(f"Получен колбэк: {event.callback_query.data}")

        # Логирование хэндлеров
        try:
            result = await handler(event, data)
            if self.log_handlers:
                alogger.info(f"Хэндлер выполнен: {handler.__name__}")
            return result
        except Exception as e:
            if self.log_errors:
                self.log_error(e)
            return None

    # Метод для логирования ошибок
    @staticmethod
    def log_error(e):
        error_message = f'Ошибка: {str(e)}'
        alogger.error(error_message)

        # Получаем информацию о строке, где произошла ошибка
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)

        if tb:
            filename, lineno, funcname, _ = tb[-1]
            error_location = f'Ошибка произошла в файле: {filename.split("\\")[-1]}, строка: {lineno}, в функции: {funcname}'
            alogger.error(error_location)

        # Отправка сообщения об ошибке в админ-группу
        # if 'message' in data and data['message'] is not None:
        #     await data['message'].bot.send_message(chat_id=BLUIXCODE_ADMIN_GROUP, text=error_message)
