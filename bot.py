import os
from flask import Flask, request
import openai
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# Load secrets from environment
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize Flask app and Telegram bot
app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Setup global dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(
    MessageHandler(Filters.text & ~Filters.command, lambda update, context: handle_message(update, context))
)

# Telegram message handler
def handle_message(update: Update, context: CallbackContext):
    user_msg = update.message.text

    try:
        # Call OpenAI ChatCompletion (correct SDK usage)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Aira, a sweet and intelligent Indian girl who replies warmly and naturally."
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = response.choices[0].message.content.strip()
        update.message.reply_text(reply)

    except Exception as e:
        print(f"OpenAI Error: {e}")
        update.message.reply_text("Sorry, there was an error processing your request.")

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Basic test route
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"
