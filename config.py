import os
from dotenv import load_dotenv

# загружаем .env
load_dotenv()

# токен бота
TOKEN = os.getenv("BOT_TOKEN")

# подключение к бд PostgreSQL
DATABASE_URL =  os.getenv("DATABASE_URL")

# телеграм оператора
OPERATOR_CHAT_ID = os.getenv("OPERATOR_CHAT_ID")


