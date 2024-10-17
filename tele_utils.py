from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_PYTHON_GUIDANCE_API_KEY = os.getenv("TELEGRAM_BOT_PYTHON_GUIDANCE_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /start command. Prints the chat_id when the command is received.
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")
    print(f"Chat ID: {chat_id}")

if __name__ == "__main__":
    # Create the application and pass the bot token
    application = ApplicationBuilder().token(TELEGRAM_BOT_PYTHON_GUIDANCE_API_KEY).build()

    # Register the /start command handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Start the bot
    print("Bot is running...")
    application.run_polling()
