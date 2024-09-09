import os
import telebot
from telebot.apihelper import ApiTelegramException
from telebot import types
import requests
import time
import logging
from functools import partial
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOT_TOKEN = 'your bot token'
CHAT_ID = 'your channel id'
USERS_FILE = 'users.json'

bot = telebot.TeleBot(BOT_TOKEN)

# Coin configuration
COINS = {
    'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance', 'DOGE': 'Doge',
    'TRX': 'Tron', 'MATIC': 'Matic', 'SOL': 'Solana', 'FTM': 'Fantom',
    'OP': 'Optimism', 'SHIB': 'Shiba'
}

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

users = load_users()

def is_subscribed(chat_id, user_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status != 'left'
    except ApiTelegramException as e:
        return e.result_json['description'] != 'Bad Request: chat not found'

def create_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(f"/{coin} {name} 💰") for coin, name in COINS.items()]
    markup.add(*buttons)
    return markup

def format_price_message(symbol, price):
    rounded_price = round(float(price), 2)
    return f"💰 {symbol} Price 💰\n\n💲 {rounded_price:,.2f} USDT\n\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        users[user_id] = {
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'join_date': time.ctime()
        }
        save_users(users)
        logger.info(f"New user added: {user_id}")

    welcome_message = (
        f"Hello {message.from_user.first_name}! 👋\n\n"
        "Welcome to Crypto Tracker Bot 🚀\n\n"
        "🔹 Get real-time crypto prices\n"
        "🔹 Use buttons or type /<coin> for prices\n"
        "🔹 /price for popular coins\n"
        "🔹 /help for more information\n\n"
        "Stay updated with market trends! 📈"
    )
    
    if not is_subscribed(CHAT_ID, message.chat.id):
        bot.reply_to(message, welcome_message + f"\n\n⚠️ Please join our group to use the bot: {CHAT_ID}")
    else:
        markup = create_markup()
        bot.reply_to(message, welcome_message, reply_markup=markup)

def send_crypto_price(message, symbol):
    if not is_subscribed(CHAT_ID, message.chat.id):
        bot.send_message(message.chat.id, f"⚠️ Please join our group to use the bot: {CHAT_ID}")
    else:
        try:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT")
            data = response.json()
            bot.send_message(message.chat.id, format_price_message(data['symbol'], data['price']))
        except requests.RequestException as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            bot.send_message(message.chat.id, f"❌ Error fetching price for {symbol}. Please try again later.")

for coin in COINS.keys():
    bot.message_handler(commands=[coin])(partial(send_crypto_price, symbol=coin))

@bot.message_handler(commands=['gpPrice'])
def group_instructions(message):
    instructions = (
        "📢 To use this bot in your group:\n\n"
        f"1️⃣ Join our group: {CHAT_ID}\n"
        "2️⃣ Add the bot to your group and make it an admin\n"
        "3️⃣ In your group, type /SetOGP"
    )
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['price'])
def popular_prices(message):
    if not is_subscribed(CHAT_ID, message.chat.id):
        bot.send_message(message.chat.id, f"⚠️ Please join our group to use the bot: {CHAT_ID}")
        return

    try:
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
        prices_message = "📊 Popular Cryptocurrency Prices 📊\n\n"
        
        for symbol in symbols:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
            data = response.json()
            rounded_price = round(float(data['price']), 2)
            prices_message += f"{symbol[:-4]}: ${rounded_price:,.2f} USDT\n"
            time.sleep(0.5)  # Add a small delay between requests
        
        prices_message += f"\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"
        bot.send_message(message.chat.id, prices_message)
    except requests.RequestException as e:
        logger.error(f"Error fetching prices: {e}")
        bot.send_message(message.chat.id, "❌ Error fetching prices. Please try again later.")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🤖 Crypto Tracker Bot Help 🤖\n\n"
        "Available commands:\n"
        "🔹 /start - Start the bot and see options\n"
        "🔹 /price - Get prices for BTC, ETH, and BNB\n"
        "🔹 /gpPrice - Instructions for group use\n"
        "🔹 /<coin> - Get price for a specific coin\n"
        "   (e.g., /BTC, /ETH, /BNB)\n\n"
        "Need more help? Contact @scream_hash"
    )
    bot.send_message(message.chat.id, help_text)

if __name__ == "__main__":
    logger.info("Bot started")
    bot.polling(none_stop=True)


#     import os
# import telebot
# from telebot.apihelper import ApiTelegramException
# from telebot import types
# import requests
# import time
# import logging
# from functools import partial
# import json


# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# BOT_TOKEN = '5596645259:AAE2G1n_3S0lAKdWPc1sggvEQ5VKhd3mXxQ'
# CHAT_ID = '@am4ha3kd'
# USERS_FILE = 'users.json'

# bot = telebot.TeleBot(BOT_TOKEN)


# COINS = {
#     'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance', 'DOGE': 'Doge',
#     'TRX': 'Tron', 'MATIC': 'Matic', 'SOL': 'Solana', 'FTM': 'Fantom',
#     'OP': 'Optimism', 'SHIB': 'Shiba'
# }

# def load_users():
#     if os.path.exists(USERS_FILE):
#         with open(USERS_FILE, 'r') as f:
#             return json.load(f)
#     return {}

# def save_users(users):
#     with open(USERS_FILE, 'w') as f:
#         json.dump(users, f)

# users = load_users()

# def is_subscribed(chat_id, user_id):
#     try:
#         return bot.get_chat_member(chat_id, user_id).status != 'left'
#     except ApiTelegramException as e:
#         return e.result_json['description'] != 'Bad Request: chat not found'

# def create_markup():
#     markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     buttons = [types.KeyboardButton(f"/{coin} {name} 💰") for coin, name in COINS.items()]
#     markup.add(*buttons)
#     return markup

# def format_price_message(symbol, price):
#     rounded_price = round(float(price), 2)
#     return f"💰 {symbol} Price 💰\n\n💲 {rounded_price:,.2f} USDT\n\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"

# @bot.message_handler(commands=['start'])
# def start_command(message):
#     user_id = str(message.from_user.id)
#     if user_id not in users:
#         users[user_id] = {
#             'username': message.from_user.username,
#             'first_name': message.from_user.first_name,
#             'last_name': message.from_user.last_name,
#             'join_date': time.ctime()
#         }
#         save_users(users)
#         logger.info(f"New user added: {user_id}")

#     welcome_message = (
#         f"Hello {message.from_user.first_name}! 👋\n\n"
#         "Welcome to CryptoPulse Bot 🚀\n\n"
#         "🔹 Get real-time crypto prices\n"
#         "🔹 Use buttons or type /<coin> for prices\n"
#         "🔹 /price for popular coins\n"
#         "🔹 /help for more information\n\n"
#         "Stay updated with market trends! 📈"
#     )
    
#     if not is_subscribed(CHAT_ID, message.chat.id):
#         bot.reply_to(message, welcome_message + "\n\n⚠️ Please join our group to use the bot: https://t.me/am4ha3kd")
#     else:
#         markup = create_markup()
#         bot.reply_to(message, welcome_message, reply_markup=markup)

# def send_crypto_price(message, symbol):
#     if not is_subscribed(CHAT_ID, message.chat.id):
#         bot.send_message(message.chat.id, "⚠️ Please join our group to use the bot: https://t.me/am4ha3kd")
#     else:
#         try:
#             response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT")
#             data = response.json()
#             bot.send_message(message.chat.id, format_price_message(data['symbol'], data['price']))
#         except requests.RequestException as e:
#             logger.error(f"Error fetching price for {symbol}: {e}")
#             bot.send_message(message.chat.id, f"❌ Error fetching price for {symbol}. Please try again later.")

# for coin in COINS.keys():
#     bot.message_handler(commands=[coin])(partial(send_crypto_price, symbol=coin))

# @bot.message_handler(commands=['gpPrice'])
# def group_instructions(message):
#     instructions = (
#         "📢 To use this bot in your group:\n\n"
#         "1️⃣ Join our group: https://t.me/am4ha3kd\n"
#         "2️⃣ Add the bot to your group and make it an admin\n"
#         "3️⃣ In your group, type /SetOGP"
#     )
#     bot.reply_to(message, instructions)

# @bot.message_handler(commands=['price'])
# def popular_prices(message):
#     if not is_subscribed(CHAT_ID, message.chat.id):
#         bot.send_message(message.chat.id, "⚠️ Please join our group to use the bot: https://t.me/am4ha3kd")
#         return

#     try:
#         symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
#         prices_message = "📊 Popular Cryptocurrency Prices 📊\n\n"
        
#         for symbol in symbols:
#             response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
#             data = response.json()
#             rounded_price = round(float(data['price']), 2)
#             prices_message += f"{symbol[:-4]}: ${rounded_price:,.2f} USDT\n"
#             time.sleep(0.5)  # Add a small delay between requests
        
#         prices_message += f"\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}"
#         bot.send_message(message.chat.id, prices_message)
#     except requests.RequestException as e:
#         logger.error(f"Error fetching prices: {e}")
#         bot.send_message(message.chat.id, "❌ Error fetching prices. Please try again later.")

# @bot.message_handler(commands=['help'])
# def help_command(message):
#     help_text = (
#         "🤖 CryptoPulse Bot Help 🤖\n\n"
#         "Available commands:\n"
#         "🔹 /start - Start the bot and see options\n"
#         "🔹 /price - Get prices for BTC, ETH, and BNB\n"
#         "🔹 /gpPrice - Instructions for group use\n"
#         "🔹 /<coin> - Get price for a specific coin\n"
#         "   (e.g., /BTC, /ETH, /BNB)\n\n"
#         "Need more help? Contact @scream_hash"
#     )
#     bot.send_message(message.chat.id, help_text)

# if __name__ == "__main__":
#     logger.info("Bot started")
#     bot.polling(none_stop=True)
