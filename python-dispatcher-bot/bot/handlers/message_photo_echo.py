from bot.handler import Handler
import bot.telegram_api_client

class MessagePhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]
    
    def handle(self, update: dict) -> bool: 
        bot.telegram_api_client.sendPhoto(
        chat_id=update["message"]["chat"]["id"],
        caption=update["message"]["caption"],
        photo=update["message"]["photo"][-1]["file_id"],
        )

        return False