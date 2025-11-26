import json

from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class OrderApprovalHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_approve", "order_restart"]

    def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        messenger.answer_callback_query(update["callback_query"]["id"])
        messenger.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_approve":
            storage.update_user_state(telegram_id, "ORDER_FINISHED")

            pizza_name = data.get("pizza_name", "Unknown")
            pizza_size = data.get("pizza_size", "Unknown")
            drink = data.get("drink", "Unknown")

            order_confirmation = f"""
✅ <b>Order Confirmed!</b>
🍕 <u>Your Order:</u>
• <b>Pizza:</b> {pizza_name}
• <b>Size:</b> {pizza_size}
• <b>Drink:</b> {drink}

Thank you for your order! Your pizza will be ready soon. (and we will eat it 😋)

Send /start to place <i>another</i> order.
"""

            messenger.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_confirmation,
                parse_mode="HTML",
            )
        elif callback_data == "order_restart":
            storage.clear_user_data(telegram_id)

            storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            messenger.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Please choose pizza type",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Margherita",
                                    "callback_data": "pizza_margherita",
                                },
                                {
                                    "text": "Pepperoni",
                                    "callback_data": "pizza_pepperoni",
                                },
                            ],
                            [
                                {
                                    "text": "Quattro Stagioni",
                                    "callback_data": "pizza_quattro_stagioni",
                                },
                                {
                                    "text": "Capricciosa",
                                    "callback_data": "pizza_capricciosa",
                                },
                            ],
                            [
                                {"text": "Diavola", "callback_data": "pizza_diavola"},
                                {
                                    "text": "Prosciutto",
                                    "callback_data": "pizza_prosciutto",
                                },
                            ],
                        ],
                    },
                ),
            )
        return HandlerStatus.STOP
