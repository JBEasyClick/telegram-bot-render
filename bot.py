import os
import openai
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# Load API keys
TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Initialize APIs
openai.api_key = OPENAI_API_KEY
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Dispatcher setup
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: handle_message(update, context)))

# Handle messages
def handle_message(update: Update, context: CallbackContext):
    user_msg = update.message.text
    print("User:", user_msg)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Aira, a sweet and intelligent Indian girl who replies warmly and naturally."},
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response.choices[0].message["content"].strip()
    print("Bot:", reply)
    update.message.reply_text(reply)

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Health check
@app.route("/")
def index():
    return "Bot is running!"
