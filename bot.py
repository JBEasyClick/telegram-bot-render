import os
import openai
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# Set environment variables
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

# Setup Flask and Telegram Bot
app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Global Dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: handle_message(update, context)))

# Message Handler
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        # Create prompt for GPT
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Aira, a sweet and intelligent Indian girl who replies warmly and naturally."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message.content.strip()
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("Sorry, there was an error processing your request.")
        print(f"OpenAI Error: {e}")

# Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Root Test Route
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"
