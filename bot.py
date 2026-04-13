import telebot
from telebot import types
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run).start()

TOKEN = "8608282848:AAFrO6m5fknvBHQxlSg4kAUaCdeB0ixEdCM"
ADMIN_ID = 6748893449

bot = telebot.TeleBot(TOKEN)

banned_users = set()

# --- МЕНЮ ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        "📩 Связь",
        "💰 Заказать бота",
        "ℹ️ Информация",
        "⚙️ Возможности",
        "👤 О владельце"
    )
    return markup


def back_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙 Назад")
    return markup


# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\n"
        "Это бот-помощник владельца @LitomaInter\n\n"
        "Если владелец занят — напишите сюда 📩",
        reply_markup=main_menu()
    )


# --- КНОПКИ ---
@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.chat.id

    if user_id in banned_users:
        return

    text = message.text

    if text == "📩 Связь":
        bot.send_message(
            user_id,
            "📩 Связь с владельцем\n\n"
            "Напишите сообщение и оно будет отправлено.\n\n"
            "— без спама\n— по делу",
            reply_markup=back_menu()
        )

    elif text == "💰 Заказать бота":
        bot.send_message(
            user_id,
            "💰 Заказ бота\n\n"
            "Опишите:\n"
            "— что должен делать бот\n"
            "— пример (если есть)\n\n"
            "Я передам владельцу 👇",
            reply_markup=back_menu()
        )

    elif text == "ℹ️ Информация":
        bot.send_message(
            user_id,
            "ℹ️ Этот бот для связи с владельцем.",
            reply_markup=back_menu()
        )

    elif text == "⚙️ Возможности":
        bot.send_message(
            user_id,
            "⚙️ Возможности:\n— связь\n— удобство",
            reply_markup=back_menu()
        )

    elif text == "👤 О владельце":
        bot.send_message(
            user_id,
            "👤 О владельце\n\n"
            "Разработчик Telegram-ботов 🤖\n\n"
            "Создаёт ботов:\n"
            "— для заработка\n"
            "— для бизнеса\n"
            "— автоматизация\n\n"
            "Пишите через 'Связь'",
            reply_markup=back_menu()
        )

    elif text == "🔙 Назад":
        bot.send_message(user_id, "🔙 Вы вернулись в меню", reply_markup=main_menu())

    else:
        bot.send_message(
            ADMIN_ID,
            f"📩 Новое сообщение\n\n"
            f"👤 ID: {user_id}\n"
            f"💬 {text}"
        )

        bot.send_message(
            user_id,
            "✅ Сообщение отправлено!\n\n⏳ Ожидайте ответа владельца."
        )


# --- ОТВЕТ АДМИНА ---
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def admin_reply(message):
    if message.reply_to_message:
        try:
            lines = message.reply_to_message.text.split("\n")
            user_id = int(lines[2].replace("👤 ID: ", ""))

            bot.send_message(user_id, f"💬 Ответ владельца:\n\n{message.text}")
        except:
            bot.send_message(ADMIN_ID, "❌ Ошибка ответа")


# --- БАН ---
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.chat.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        banned_users.add(user_id)
        bot.send_message(ADMIN_ID, f"🚫 Пользователь {user_id} забанен")
    except:
        bot.send_message(ADMIN_ID, "❌ Используй: /ban ID")


bot.polling(none_stop=True)
