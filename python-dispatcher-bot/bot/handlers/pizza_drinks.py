import json

import bot.telegram_api_client
import bot.database_client
from bot.handlers.handler import Handler, HandlerStatus


class PizzaDrinksHandler(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink_mapping = {
            "drink_coca_cola": "Coca-Cola",
            "drink_pepsi": "Pepsi",
            "drink_orange_juice": "Orange Juice",
            "drink_apple_juice": "Apple Juice",
            "drink_water": "Water",
            "drink_iced_tea": "Iced Tea",
            "drink_none": "No drinks",
        }
        selected_drink = drink_mapping.get(callback_data)

        order_json["drink"] = selected_drink

        bot.database_client.update_user_order_json(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")

        bot.telegram_api_client.answerCallbackQuery(update["callback_query"]["id"])

        bot.telegram_api_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        pizza_name = order_json.get("pizza_name", "Unknown")
        pizza_size = order_json.get("pizza_size", "Unknown")
        drink = order_json.get("drink", "Unknown")

        order_summary = \
f"""
🍕 <u>Your Order Summary:</u>
<b>Pizza:</b> {pizza_name}
<b>Size:</b> {pizza_size}
<b>Drink:</b> {drink}

☑️ Is everything correct?
"""

        bot.telegram_api_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
            parse_mode="HTML",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "✅ Ok", "callback_data": "order_approve"},
                            {"text": "🔄 Start again", "callback_data": "order_restart"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP