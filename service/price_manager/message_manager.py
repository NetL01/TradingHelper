import os

class MessageManager:
    message_id_file = 'data/message_id.txt'

    @staticmethod
    def load_message_id():
        if os.path.exists(MessageManager.message_id_file):
            with open(MessageManager.message_id_file, 'r') as f:
                mid = f.read().strip()
                if mid.isdigit():
                    return int(mid)
        return None

    @staticmethod
    def save_message_id(mid):
        with open(MessageManager.message_id_file, 'w') as f:
            f.write(str(mid))

    @staticmethod
    def reset_message_id():
        if os.path.exists(MessageManager.message_id_file):
            os.remove(MessageManager.message_id_file)

    @staticmethod
    def delete_previous_message(bot, chat_id):
        message_id = MessageManager.load_message_id()
        if message_id is not None:
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Не удалось удалить предыдущее сообщение: {e}")
            MessageManager.reset_message_id()
