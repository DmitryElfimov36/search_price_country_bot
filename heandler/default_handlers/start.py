from aiogram import types, Dispatcher
import aiogram.utils.markdown as md
from create_bot import bot
from keyboard import kb_client


# функция, срабатывающая сразу при запуске бота
async def bot_start(message: types.Message):
    await bot.send_message(message.chat.id, md.text(f"Привет, *{message.from_user.full_name}*! Для поиска информации "
                                                    f"нажми кнопку *'Поиск'*\nДля подробной "
                                                    f"информации о боте нажми кнопку *'Помощь'*"),
                           reply_markup=kb_client, parse_mode='Markdown')


def register_handlers_start(db: Dispatcher):
    db.register_message_handler(bot_start)
