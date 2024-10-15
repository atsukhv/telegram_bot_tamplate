import asyncio
from aiogram import Bot, Dispatcher
from aiologger.al_settings import alogger, date_and_time_format  # Импортируем alogger и функцию форматирования
from config import BOT_TOKEN
from database.db_midleware import DataBaseSession
from database.models import async_main, session_maker
from aiologger.Aiologger import ErrorLoggingMiddleware
from app.main_handler import router as main_router

async def bot_start():
    alogger.info("Бот запущен.")


async def bot_stop():
    alogger.info("Бот остановлен.")

async def main():
    await async_main()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    # Устанавливаем форматирование для логирования
    await date_and_time_format(show_time=True, show_date=True)

    dp.update.middleware(ErrorLoggingMiddleware(log_errors=True,
                                                log_messages=True,
                                                log_handlers=True,
                                                log_callbacks=True,
                                                show_time=False,
                                                show_date=False,
                                                ))

    dp.include_routers(main_router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot_start()  # Отправка сообщения при запуске бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot_stop()  # Отправка сообщения при завершении работы бота
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
