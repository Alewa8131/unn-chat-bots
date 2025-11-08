import json
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()


def recreate_database() -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_DB_PATH"))
    with connection:
        connection.execute("DROP TABLE IF EXISTS telegram_updates")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS  telegram_updates
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """,
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state TEXT DEFAULT NULL,
                order_json TEXT DEFAULT NULL
            )
            """,
        )
    connection.close()
    print(f"База данных успешно создана по пути: {os.getenv("SQLITE_DB_PATH")}")


def persist_updates(updates: dict) -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_DB_PATH"))
    with connection:
        data = []
        for update in updates:
            data.append((json.dumps(update, ensure_ascii=False, indent=2),))
        connection.executemany("INSERT INTO  telegram_updates (payload) VALUES (?)", data,)
    connection.close()


def ensure_user_exists(telegram_id: int) -> None:
    with sqlite3.connect(os.getenv("SQLITE_DB_PATH")) as connection:
        with connection:
            cursor = connection.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,)
            )

            if cursor.fetchone() is None:
                connection.execute(
                    "INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,)
                )