from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_all = InlineKeyboardButton('Все данные', callback_data='all_data')
button_food = InlineKeyboardButton('Еда', callback_data='food')
button_housing = InlineKeyboardButton('Жилье', callback_data='housing')
button_transport = InlineKeyboardButton('Транспорт', callback_data='transport')
kb_choice = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_choice.add(button_all).add(button_food).insert(button_housing).insert(button_transport)

