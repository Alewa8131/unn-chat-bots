from bot.dispatcher import Dispatcher
from bot.handlers.message_text_echo import MessageTextEcho
from bot.handlers.message_photo_echo import MessagePhotoEcho
from bot.handlers.database_logger import DatabaseLogger
from bot.long_polling import start_long_polling


if __name__ == "__main__":
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handler(DatabaseLogger())
        dispatcher.add_handler(MessagePhotoEcho())
        dispatcher.add_handler(MessageTextEcho())
        start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")
