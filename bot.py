import os
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext
from openai import OpenAI

# Environment Variables
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# OpenAI Client (v1+ style)
client = OpenAI(api_key=OPENAI_API_KEY)

# Telegram Bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Flask App
app = Flask(__name__)

# Message Handler
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
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
        print(f"OpenAI Error: {e}")
        update.message.reply_text("Sorry, something went wrong. Please try again later.")

# Dispatcher Setup
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Health Check
@app.route("/", methods=["GET"])
def index():
    return "Bot is live!"
