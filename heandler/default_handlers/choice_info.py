from aiogram import types, Dispatcher
import aiogram.utils.markdown as md
from create_bot import bot, db
from keyboard import kb_choice


@db.message_handler(text='Поиск')
async def choice_info_bot(message: types.Message):
    await bot.send_message(message.chat.id, md.text(f"Выберите формат вывода: "), reply_markup=kb_choice)


def register_handlers_search(db: Dispatcher):
    db.register_message_handler(choice_info_bot, commands=['Поиск'])
