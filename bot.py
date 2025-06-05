import telebot
import threading
from price_manager import PriceManager
from config import TOKEN, CHAT_ID
import time

bot = telebot.TeleBot(TOKEN)
price_manager = PriceManager(bot, CHAT_ID)

def main():
    print("BOT STARTED", time.time())
    price_manager.delete_previous_message()
    price_manager.reset_message_id()

    threading.Thread(target=price_manager.start_price_updates, daemon=True).start()

    bot.infinity_polling()

if __name__ == '__main__':
    main()
