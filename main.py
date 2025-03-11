import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiohttp import web
from tortoise import Tortoise

from bot.handlers import register_all_handlers
from config import TOKEN, init_db, USE_WEBHOOK, WEBHOOK_PATH, WEBHOOK_URL, WEBHOOK_SECRET, WEB_SERVER_HOST, \
    WEB_SERVER_PORT

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

async def on_startup(bot: Bot):
    """Функция, которая выполняется при запуске бота."""
    await init_db()
    logging.info("База данных инициализирована")

    if USE_WEBHOOK:
        # Установка webhook
        await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
        logging.info(f"Webhook установлен: {WEBHOOK_URL}")

    logging.info("Бот запущен и инициализирован.")


async def on_shutdown(bot: Bot):
    """Функция, которая выполняется при выключении бота."""
    logging.info("Бот выключается...")

    await Tortoise.close_connections()


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    register_all_handlers(dp)

    # Регистрируем хуки старта и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if USE_WEBHOOK:
        app = web.Application()
        webhook_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        webhook_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        logging.info(f"Запуск веб-сервера для webhook на {WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    else:
        logging.info("Запуск бота в режиме long polling")
        await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")
        sys.exit(0)
