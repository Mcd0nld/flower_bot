from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from sqlalchemy.orm import sessionmaker
from database import engine, Customer
from config import OPERATOR_CHAT_ID

# cоздаем сессию для работы с бд
Session = sessionmaker(bind=engine)

# определяем состояния
ASK_NAME, ASK_BIRTHDAY, ASK_PHONE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие пользователя"""
    await update.message.reply_text("Привет! Как тебя зовут?")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос имени пользователя"""
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Отлично! Теперь укажи свою дату рождения (ГГГГ-ММ-ДД):")
    return ASK_BIRTHDAY

async def ask_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос даты рождения пользователя"""
    context.user_data["birth_date"] = update.message.text
    await update.message.reply_text("Теперь введи свой номер телефона (+7):")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос номера телефона и сохранение данных пользователя"""
    context.user_data["phone_number"] = update.message.text

    # сохранение данных в бд
    session = Session()
    customer = Customer(
        name = context.user_data["name"],
        birth_date = context.user_data["birth_date"],
        phone_number = context.user_data["phone_number"]
    )
    session.add(customer)
    session.commit()
    session.close()

    # уведомление оператора
    await context.bot.send_message(
        chat_id=OPERATOR_CHAT_ID,
        text=f"📩 Новый клиент!\nИмя: {context.user_data['name']}\nДата рождения: {context.user_data['birth_date']}\nТелефон: {context.user_data['phone_number']}"
    )

    await update.message.reply_text("Спасибо! Наш оператор скоро с вами свяжется. @FiorePerAmore1")
    return ConversationHandler.END


