import os
from dotenv import load_dotenv
from tortoise import Tortoise


load_dotenv()


TOKEN = os.getenv("TOKEN_BOT")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

USE_WEBHOOK = os.getenv("USE_WEBHOOK", "False").lower() in ("true", "1")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "127.0.0.1")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my-secret")
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL", "")
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
WEB_SERVER_PORT = int(os.getenv("PORT", 3000))


async def init_db():
    await Tortoise.init(
        db_url='sqlite://database/kernal.sqlite3',
        modules={'models': ['bot.crud.models']}
    )
    await Tortoise.generate_schemas()