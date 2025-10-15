import time

import bot.database_client
import bot.telegram_api_client


def main() -> None:
    try:
        next_update_offset = 0
        while True:
            updates = bot.telegram_api_client.getUpdates(next_update_offset)
            bot.database_client.persist_updates(updates)
            for update in updates:
                bot.telegram_api_client.sendMessage(
                    chat_id=update["message"]["chat"]["id"],
                    text=update["message"]["text"],
                )
                next_update_offset = max(next_update_offset, update["update_id"] + 1)
                print(".", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
