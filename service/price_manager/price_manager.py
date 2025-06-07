import time
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
        message_id = MessageManager.load_message_id()

        try:
            if message_id is None or force_new_message:
                MessageManager.delete_previous_message(self.bot, self.chat_id)
                sent = self.bot.send_message(self.chat_id, text)
                MessageManager.save_message_id(sent.message_id)
                self.last_sent_time = now
            else:
                self.bot.edit_message_text(text, self.chat_id, message_id)
        except Exception as e:
            print("Ошибка отправки или редактирования сообщения:", e)

    def start_price_updates(self):
        while True:
            self.send_price_message()
            time.sleep(30)
