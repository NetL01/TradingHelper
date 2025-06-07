import telebot
import threading
import time

from service.price_manager.message_manager import MessageManager
from service.price_manager.price_manager import PriceManager
from config import TOKEN, CHAT_ID

bot = telebot.TeleBot(TOKEN)
price_manager = PriceManager(bot, CHAT_ID)

def main():
    print("BOT STARTED", time.time())
    MessageManager.delete_previous_message(bot, CHAT_ID)
    MessageManager.reset_message_id()
    threading.Thread(target=price_manager.start_price_updates, daemon=True).start()

    bot.infinity_polling()

if __name__ == '__main__':
    main()
