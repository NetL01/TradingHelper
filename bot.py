import telebot
import threading
import time

from service.price_manager.message_manager import MessageManager
from service.price_manager.price_manager import PriceManager
from config import TOKEN, CHAT_ID

bot = telebot.TeleBot(TOKEN)
price_manager = PriceManager(bot, CHAT_ID)

@bot.message_handler(commands=['start'])
def start(message):
    print("Chat ID:", message.chat.id)
    bot.send_message(message.chat.id, "Привет!")


@bot.message_handler(commands=['addprice'])
def handle_addprice(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❗ Укажите монету: /addprice <coin>")
        return
    coin = parts[1]
    result = price_manager.add_price_coin(coin)
    bot.reply_to(message, result)

@bot.message_handler(commands=['delprice'])
def handle_delprice(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❗ Укажите монету: /delprice <coin>")
        return
    coin = parts[1]
    result = price_manager.del_price_coin(coin)
    bot.reply_to(message, result)



def main():
    print("BOT STARTED", time.time())
    MessageManager.delete_previous_message(bot, CHAT_ID)
    MessageManager.reset_message_id()
    threading.Thread(target=price_manager.start_price_updates, daemon=True).start()

    bot.infinity_polling()

if __name__ == '__main__':
    main()
