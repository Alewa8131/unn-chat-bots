from bot.handlers.handler import Handler
from bot.handlers.database_logger import DatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.message_photo_echo import MessagePhotoEcho
from bot.handlers.message_text_echo import MessageTextEcho

def get_handlers() -> list[Handler]:
    return [
        DatabaseLogger(),
        EnsureUserExists(),
        MessageTextEcho(),
        MessagePhotoEcho(),
    ]