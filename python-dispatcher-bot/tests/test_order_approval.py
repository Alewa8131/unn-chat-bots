from bot.dispatcher import Dispatcher
from bot.handlers.order_approval import OrderApprovalHandler

from tests.mocks import Mock
import json


def test_order_approval_success():
    test_update = {
        "update_id": 123456790,
        "callback_query": {
            "id": 1,
            "from": {"id": 12345, "is_bot": False, "username": "testuser"},
            "message": {
                "message_id": 101,
                "date": 1640995200,
                "chat": {"id": 12345, "type": "private"},
                "text": "Your order is ready for approval.",
            },
            "data": "order_approve",
        },
    }

    test_data = {
        "pizza_name": "Margherita",
        "pizza_size": "Large",
        "drink": "Cola",
    }

    update_user_state_called = False
    answer_callback_query_called = False
    delete_message_called = False
    send_message_calls = []

    def update_user_state(telegram_id: int, state: str) -> None:
        nonlocal update_user_state_called
        update_user_state_called = True
        assert telegram_id == 12345
        assert state == "ORDER_FINISHED"

    def get_user(telegram_id: int) -> dict | None:
        return {"state": "WAIT_FOR_ORDER_APPROVE", "data": json.dumps(test_data)}

    mock_storage = Mock(
        {
            "update_user_state": update_user_state,
            "get_user": get_user,
        }
    )

    def answer_callback_query(callback_query_id: str, **params) -> dict:
        nonlocal answer_callback_query_called
        answer_callback_query_called = True
        assert callback_query_id == 1
        return {"ok": True}

    def delete_message(chat_id: int, message_id: int) -> dict:
        nonlocal delete_message_called
        delete_message_called = True
        assert chat_id == 12345
        assert message_id == 101
        return {"ok": True}

    def send_message(chat_id: int, text: str, **params) -> dict:
        assert chat_id == 12345
        send_message_calls.append({"text": text, "params": params})
        return {"ok": True}

    mock_messenger = Mock(
        {
            "answer_callback_query": answer_callback_query,
            "delete_message": delete_message,
            "send_message": send_message,
        }
    )

    dispatcher = Dispatcher(mock_storage, mock_messenger)

    dispatcher.add_handler(OrderApprovalHandler())

    dispatcher.dispatch(test_update)

    assert update_user_state_called
    assert answer_callback_query_called
    assert delete_message_called

    assert len(send_message_calls) == 1

    assert "✅ <b>Order Confirmed!</b>" in send_message_calls[0]["text"]
    assert (
        test_data["pizza_name"]
        and test_data["pizza_size"]
        and test_data["drink"] in send_message_calls[0]["text"]
    )
    assert send_message_calls[0]["params"]["parse_mode"] == "HTML"
