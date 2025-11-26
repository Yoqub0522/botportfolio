import os
import random
from flask import Flask, request
import telebot
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji
)

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Web App URLs
WEB_URL = "https://taklifnoma.yoqubaxmedov.xyz/"
WEB_URL2 = "https://edueyesio.yoqubaxmedov.xyz/"
WEB_URL3 = "https://faceid.yoqubaxmedov.xyz/"
GitHub = "https://github.com/Yoqub0522"

# Flask App
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200


@bot.message_handler(commands=["start"])
def start(message):
    reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard_markup.row(KeyboardButton("Taklifnoma", web_app=WebAppInfo(WEB_URL)))
    reply_keyboard_markup.row(KeyboardButton("Edueyes", web_app=WebAppInfo(WEB_URL2)))
    reply_keyboard_markup.row(KeyboardButton("Faceid", web_app=WebAppInfo(WEB_URL3)))
    reply_keyboard_markup.row(KeyboardButton('GitHub', web_app=WebAppInfo(GitHub)))

    inline_keyboard_markup = InlineKeyboardMarkup()
    inline_keyboard_markup.row(InlineKeyboardButton('Taklifnoma', web_app=WebAppInfo(WEB_URL)))
    inline_keyboard_markup.row(InlineKeyboardButton('Edueyes', web_app=WebAppInfo(WEB_URL2)))
    inline_keyboard_markup.row(InlineKeyboardButton('Faceid', web_app=WebAppInfo(WEB_URL3)))
    inline_keyboard_markup.row(InlineKeyboardButton('GitHub', web_app=WebAppInfo(GitHub)))

    bot.send_message(message.chat.id, "Inline tugmalar", reply_markup=inline_keyboard_markup)
    bot.send_message(message.chat.id, "Xoxlasang tugmalarni menudan bos", reply_markup=reply_keyboard_markup)


@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    bot.reply_to(message, f'Your message is "{message.web_app_data.data}"')


@bot.message_handler(func=lambda message: True)
def send_reaction(message):
    emo = ["🔥", "🤗", "😎"]
    bot.set_message_reaction(
        message.chat.id,
        message.id,
        [ReactionTypeEmoji(random.choice(emo))],
        is_big=False
    )


@bot.message_reaction_handler(func=lambda msg: True)
def get_reactions(message):
    bot.reply_to(
        message,
        f"You changed the reaction from {[r.emoji for r in message.old_reaction]} "
        f"to {[r.emoji for r in message.new_reaction]}"
    )


# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
