from bot.handler import Handler
import bot.database_client

class DatabaseLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update
    
    def handle(self, update: dict) -> bool: 
        bot.database_client.persist_update(update)
        return True