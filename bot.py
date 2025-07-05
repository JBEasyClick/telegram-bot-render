import os
import openai
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# Load environment variables
TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# Initialize Flask and Telegram bot
app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

# Initialize the dispatcher once (global scope)
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(
    MessageHandler(Filters.text & ~Filters.command, lambda update, context: handle_message(update, context))
)

# Route for Telegram webhook
@app.route('/webhook', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Telegram message handler
def handle_message(update: Update, context: CallbackContext):
    user_msg = update.message.text

    prompt = f"You are Aira, a sweet and intelligent Indian girl who replies warmly and naturally. Respond to this: {user_msg}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].text.strip()
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("Sorry, there was an error processing your request.")
        print(f"OpenAI Error: {e}")

# Route to confirm server is running
@app.route('/')
def index():
    return "Bot is running!"
