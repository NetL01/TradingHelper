# price_manager.py

import time
import os
import requests
from beauty.format_nice_output import format_nice_output
from service.fetchers.get_fear_greed_index import get_fear_greed_index

from service.fetchers.get_price_coingecko import get_price_coingecko
from service.fetchers.get_price_binance import get_price_binance


class PriceManager:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id_file = 'data/message_id.txt'
        self.message_id = self.load_message_id()
        self.last_sent_time = 0


    def load_message_id(self):
        if os.path.exists(self.message_id_file):
            with open(self.message_id_file, 'r') as f:
                mid = f.read().strip()
                if mid.isdigit():
                    return int(mid)
        return None

    def save_message_id(sprelf, mid):
        with open(self.message_id_file, 'w') as f:
            f.write(str(mid))
        self.message_id = mid

    def reset_message_id(self):
        self.message_id = None
        if os.path.exists(self.message_id_file):
            os.remove(self.message_id_file)

    def delete_previous_message(self):
        if self.message_id is not None:
            try:
                self.bot.delete_message(self.chat_id, self.message_id)
            except Exception as e:
                print(f"Не удалось удалить предыдущее сообщение: {e}")
            self.message_id = None
            if os.path.exists(self.message_id_file):
                os.remove(self.message_id_file)

    def get_prices(self):
        prices = {
            'BTCUSDT': get_price_coingecko('bitcoin'),
            'SUIUSDT': get_price_binance('SUIUSDT'),
            'TRUMPUSDT': get_price_binance('TRUMPUSDT'),
        }
        return {k: v for k, v in prices.items() if v is not None}

    def send_price_message(self):
        prices = self.get_prices()
        text = format_nice_output(prices, {})
        text += "\n\n" + get_fear_greed_index()

        now = time.time()
        force_new_message = now - self.last_sent_time > 1800

        try:
            if self.message_id is None or force_new_message:
                self.delete_previous_message()
                sent = self.bot.send_message(self.chat_id, text)
                self.save_message_id(sent.message_id)
                self.last_sent_time = now
            else:
                self.bot.edit_message_text(text, self.chat_id, self.message_id)
        except Exception as e:
            print("Ошибка отправки или редактирования сообщения:", e)

    def start_price_updates(self):
        while True:
            self.send_price_message()
            time.sleep(30)
