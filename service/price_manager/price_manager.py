import time
import json
import os
from beauty.format_nice_output import format_nice_output
from service.fetchers.get_fear_greed_index import get_fear_greed_index
from service.fetchers.get_price_coingecko import get_price_coingecko
from service.fetchers.get_price_binance import get_price_binance
from service.price_manager.message_manager import MessageManager


class PriceManager:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id
        self.last_sent_time = 0
        self.coins_file = 'data/checked_coins.json'
        self.ensure_file_exists()
        self.message_id = MessageManager.load_message_id()

    def ensure_file_exists(self):
        if not os.path.exists(self.coins_file):
            with open(self.coins_file, 'w') as f:
                json.dump([], f)

    def load_tracked_coins(self):
        with open(self.coins_file, 'r') as f:
            return json.load(f)

    def save_tracked_coins(self, coins):
        with open(self.coins_file, 'w') as f:
            json.dump(coins, f, indent=2)

    def get_prices(self):
        coins = self.load_tracked_coins()
        prices = {}

        for coin in coins:
            source = coin['source']
            coin_id = coin['id']
            label = coin.get('label', coin_id)

            try:
                if source == 'coingecko':
                    price = get_price_coingecko(coin_id)
                elif source == 'binance':
                    price = get_price_binance(coin_id)
                else:
                    continue

                if price is not None:
                    prices[label] = price
            except Exception as e:
                print(f"Ошибка получения цены для {label} через {source}: {e}")

        return prices

    def send_price_message(self):
        prices = self.get_prices()
        text = format_nice_output(prices, {})
        text += "\n\n" + get_fear_greed_index()

        now = time.time()
        force_new_message = now - self.last_sent_time > 1800
        if not hasattr(self, 'message_id'):
            self.message_id = MessageManager.load_message_id()

        try:
            if self.message_id is None or force_new_message:
                MessageManager.delete_previous_message(self.bot, self.chat_id)
                self.message_id = None
                sent = self.bot.send_message(self.chat_id, text)
                MessageManager.save_message_id(sent.message_id)
                self.message_id = sent.message_id
                self.bot.pin_chat_message(self.chat_id, sent.message_id)

                self.last_sent_time = now
            else:
                self.bot.edit_message_text(text, self.chat_id, self.message_id)
        except Exception as e:
            print("Ошибка отправки или редактирования сообщения:", e)

    def start_price_updates(self):
        while True:
            self.send_price_message()
            time.sleep(30)

    def add_price_coin(self, coin_name):
        coin = coin_name.upper()
        coin_lower = coin_name.lower()

        coins = self.load_tracked_coins()
        if any(c['label'] == coin for c in coins):
            return f"⚠️ Монета {coin} уже отслеживается."

        if get_price_coingecko(coin_lower) is not None:
            source = "coingecko"
            coin_id = coin_lower
        elif get_price_binance(coin) is not None:
            source = "binance"
            coin_id = coin
        else:
            return f"❌ Не удалось найти цену по монете {coin} ни в одном источнике."

        coins.append({
            "id": coin_id,
            "label": coin,
            "source": source
        })

        self.save_tracked_coins(coins)
        return f"✅ Добавлена монета {coin} (источник: {source})"

    def del_price_coin(self, coin_name):
        coin = coin_name.upper()

        coins = self.load_tracked_coins()
        filtered = [c for c in coins if c['label'] != coin]

        if len(filtered) == len(coins):
            return f"❌ Монета {coin} не найдена в списке отслеживания."

        self.save_tracked_coins(filtered)
        return f"🗑 Монета {coin} удалена из отслеживания."

    def list_tracked_coins(self):
        coins = self.load_tracked_coins()
        return [c['label'] for c in coins]
