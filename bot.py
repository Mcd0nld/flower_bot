from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config import TOKEN
from handlers import start, ask_name, ask_birthday, ask_phone, cancel

# Определяем состояния
ASK_NAME, ASK_BIRTHDAY, ASK_PHONE = range(3)

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_birthday)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()