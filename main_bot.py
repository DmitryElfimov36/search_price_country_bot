from aiogram.utils import executor
from heandler.default_handlers import search, start, choice_info, search_food, search_transport, search_housing, helps
from create_bot import db
from data_base import sqlite_db


search.register_handlers_search(db)
start.register_handlers_start(db)
choice_info.register_handlers_search(db)
search_food.register_handlers_search(db)
search_transport.register_handlers_search(db)
search_housing.register_handlers_search(db)
helps.register_handlers_start(db)


async def on_startup(_):
    print('Бот запущен')
    await sqlite_db.sql_start()


if __name__ == "__main__":
    executor.start_polling(db, on_startup=on_startup)
