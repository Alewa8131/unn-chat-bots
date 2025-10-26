from bot.dispatcher import Dispatcher
from bot.handlers.message_echo import TextEcho, PhotoEcho
from bot.long_polling import start_long_polling


if __name__ == "__main__":
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handler(PhotoEcho())
        dispatcher.add_handler(TextEcho())
        start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")
