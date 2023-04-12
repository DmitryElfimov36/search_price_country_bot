import requests
import aiogram.utils.markdown as md
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from translate import Translator
from config import RAPID_API_KEY
from create_bot import db, bot
from data_base import sqlite_db


class Form_housing(StatesGroup):
    country = State()
    city = State()


@db.callback_query_handler(text='housing')
async def food_command(call: types.CallbackQuery):
    await Form_housing.country.set()
    await call.message.answer('Введите страну:')


@db.callback_query_handler(text='Жилье', state=Form_housing.country)
async def country_food(message: types.Message, state: FSMContext):
    translator = Translator(from_lang='ru', to_lang='en')
    async with state.proxy() as data:
        data['country'] = translator.translate(message.text)

    await Form_housing.next()
    await message.answer("Введите город:")


@db.callback_query_handler(state=Form_housing.city)
async def city_food(message: types.Message, state: FSMContext):
    translator = Translator(from_lang='ru', to_lang='en')
    async with state.proxy() as data:
        data['city'] = translator.translate(message.text)
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Страна: ', md.bold(data['country'])),
                md.text('Город:', md.bold(data['city'])),
                sep='\n'
            ))
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        country = data['country']
        city = data['city']
        button = 'Жилье'

        await sqlite_db.db_table_val(us_id=us_id, user_id=us_name, country=country, city=city, button=button)
        await state.finish()

    try:
        url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"

        querystring = {"city_name": data['city'], "country_name": data['country']}

        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "cost-of-living-and-prices.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        city = data['city_name']
        country = data['country_name']
        currency = data['prices'][0]['currency_code']
        max_outside = data['prices'][0]['max']
        usd_max_outside = data['prices'][0]['usd']['max']
        min_outside = data['prices'][0]['min']
        usd_min_outside = data['prices'][0]['usd']['min']
        max_center = data['prices'][1]['max']
        usd_max_center = data['prices'][1]['usd']['max']
        min_center = data['prices'][1]['min']
        usd_min_center = data['prices'][0]['usd']['min']
        rent_one_outside = data['prices'][25]['avg']
        usd_rent_one_outcide = data['prices'][25]['usd']['avg']
        rent_one_center = data['prices'][26]['avg']
        usd_rent_one_center = data['prices'][26]['usd']['avg']
        rent_three_outside = data['prices'][27]['avg']
        usd_rent_three_outside = data['prices'][27]['usd']['avg']
        rent_three_center = data['prices'][28]['avg']
        usd_rent_three_center = data['prices'][28]['usd']['avg']

        await bot.send_message(message.chat.id,
                               f'Выбранная страна: {country}\nВыбранный город: {city}\n\U0001F4B2 Цены указаны в местной валюте ({currency}) и в долларах (USD)\n'
                               f'\nПокупка жилья\n'
                                   f'\U0001F3E1 Стоимость покупки квартиры за пределами центра города (за 1 м²): \n'
                                   f'от {min_outside} {currency} до {max_outside} {currency};'
                                   f'\nот {usd_min_outside}$ до {usd_max_outside}$\n'
                                   f'\U0001F3E0 Стоимость покупки квартиры в центре города (за 1 м²): \n'
                                   f'от {min_center} {currency} до {max_center} {currency};\nот {usd_min_center}$ до {usd_max_center}$\n'
                               f'\nАренда жилья\n'
                                   f'\U0001F3E1 Однокомнатная квартира за пределами центра города: {rent_one_outside} {currency}; {usd_rent_one_outcide}$\n'
                                   f'\U0001F3E2 Однокомнатная квартира в центре города: {rent_one_center} {currency}, {usd_rent_one_center}$\n'
                                   f'\U0001F3E1 Трехкомнатная квартира за пределами центра города: {rent_three_outside} {currency}; {usd_rent_three_outside}$\n'
                                   f'\U0001F3E2 Трехкомнатная квартира в центре города: {rent_three_center} {currency}; {usd_rent_three_center}$\n'
                                   )
    except:
        await bot.send_message(message.chat.id, '\U00002620 Проверьте данные')


def register_handlers_search(db: Dispatcher):
    db.register_message_handler(food_command, commands=['housing'])
    db.register_message_handler(country_food, state=Form_housing.country)
    db.register_message_handler(city_food, state=Form_housing.city)
