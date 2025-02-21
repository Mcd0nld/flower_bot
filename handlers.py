from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from sqlalchemy.orm import sessionmaker
from database import engine, Customer
from config import OPERATOR_CHAT_ID
import re
from datetime import datetime

# cоздаем сессию для работы с бд
Session = sessionmaker(bind=engine)

# определяем состояния
ASK_NAME, ASK_BIRTHDAY, ASK_PHONE = range(3)

# функции валидации
def is_valid_name(name):
    """Проверка, что имя содержит только буквы"""
    return bool(re.match(r"^[А-Яа-яA-Za-z\s-]{2,50}$", name))

def is_valid_date(date_text):
    """Проверка формата даты рождения"""
    try:
        datetime.strptime(date_text, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def is_valid_phone(phone):
    """Проверка формата телефона"""
    if not isinstance(phone, str):
        return False
    return bool(re.match(r"^(\+7|8)\d{10}$", phone))

# обработчики состояний
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие пользователя"""
    await update.message.reply_text("🌸 Fiore per Amore приветствует вас! 🌸")
    await update.message.reply_text("Рады видеть вас! Мы поможем вам выбрать идеальный букет для близкого человека. 🎁💐")
    await update.message.reply_text("Как к вам обращаться?")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос имени пользователя"""
    name = update.message.text.strip()
    if not is_valid_name(name):
        await update.message.reply_text("❌ Некорректное имя..\n\nВведите имя снова, оно должно состоять только из букв.")
        return ASK_NAME
    
    context.user_data["name"] = update.message.text
    await update.message.reply_text(f"✨ Приятно познакомиться, {context.user_data['name']}!")
    await update.message.reply_text("Укажите дату своего рождения, чтобы получить возможность приобрести букет со скидкой!")
    return ASK_BIRTHDAY

async def ask_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос даты рождения пользователя"""
    bith_date = update.message.text.strip()
    if not is_valid_date(bith_date):
        await update.message.reply_text("❌ Некорректная дата..\n\nВведите дату в формате ДД.ММ.ГГГГ.")
        return ASK_BIRTHDAY

    context.user_data["birth_date"] = update.message.text
    await update.message.reply_text("🎉 Отлично! Оставьте ваш номер телефона, чтобы мы могли связаться.")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос номера телефона и сохранение данных пользователя"""
    phone_number = update.message.text.strip()
    if not is_valid_phone(phone_number):
        await update.message.reply_text("❌ Некорректный номер..\n\nВведите в формате +7XXXXXXXXXX.")
        return ASK_PHONE

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

    await update.message.reply_text(f"✅ Спасибо, {context.user_data['name']}! Теперь вы с нами, и мы всегда готовы помочь вам выбрать самые красивые цветы! 🌹")
    await update.message.reply_text("📩 Для продолжения оформления заказа, скоро с вами свяжется - @FiorePerAmore1")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик отмены"""
    await update.message.reply_text("Диалог отменен.")
    return ConversationHandler.END


