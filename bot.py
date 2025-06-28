import os
import openai
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# Setup environment
TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# Bot & Flask setup
bot = telegram.Bot(token=TOKEN)
app = Flask(name)

# Dispatcher setup (global)
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: handle_message(update, context)))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# OpenAI message handler
def handle_message(update: Update, context: CallbackContext):
    user_msg = update.message.text
    prompt = f"You are Aira, a sweet and intelligent Indian girl who replies warmly and naturally. Respond to this: {user_msg}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    reply = response.choices[0].text.strip()
    update.message.reply_text(reply)

# Test route
@app.route("/")
def index():
    return "Bot is running!"
