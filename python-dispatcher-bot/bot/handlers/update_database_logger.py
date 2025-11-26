from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class UpdateDatabaseLogger(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messanger: Messenger,
    ) -> bool:
        return "update_id" in update

    def handle(
        self,
        update: dict,
        state: str,
        order_json: dict,
        storage: Storage,
        messanger: Messenger,
    ) -> HandlerStatus:
        storage.persist_update(update)
        return HandlerStatus.CONTINUE
