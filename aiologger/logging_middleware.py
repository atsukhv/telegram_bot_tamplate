from aiogram import BaseMiddleware
from aiogram.types import Update
from loguru import logger

bot_id = 7475730659


class LoggingMiddleware(BaseMiddleware):
    bot_id = 7475730659

    async def __call__(self, handler, event: Update, data: dict):
        if event is None:
            logger.error("Событие не определено (event is None).")
            return

        # Определение пользователя и типа события
        event_type = None

        if hasattr(event, 'callback_query') and event.callback_query is not None:
            event_type = "callback_query"
            callback_data = event.callback_query.data
            logger.info(f"Callback вызван: callback_data={callback_data}")
        elif hasattr(event, 'message') and event.message is not None:
            event_type = "message"
            message_id = event.message.message_id
            text = event.message.text
            logger.info(
                f"Сообщение получено: message_id={message_id}, text={text}")
        else:
            event_type = type(event).__name__
            logger.info(f"Событие типа '{event_type}' обработано без участия пользователя.")

        # Вызов следующего middleware или обработчика
        try:
            result = await handler(event, data)
        except Exception as e:
            logger.error(f"Ошибка при вызове обработчика: {e}")
            raise

        # Логирование информации о действии после обработки
        # logger.debug(f"Событие обработано: event_type={event_type}")

        # Логирование исходящих сообщений
        if event_type == "message" and event.message.from_user.id == bot_id:
            logger.info(f"Бот отправил сообщение: message_id={event.message.message_id}, text={event.message.text}")

        return result
