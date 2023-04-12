import requests
import aiogram.utils.markdown as md
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from translate import Translator
from config import RAPID_API_KEY
from create_bot import db, bot
from data_base import sqlite_db


class Form_transport(StatesGroup):
    country = State()
    city = State()


@db.callback_query_handler(text='transport')
async def food_command(call: types.CallbackQuery):
    await Form_transport.country.set()
    await call.message.answer('Введите страну:')


@db.callback_query_handler(text='Транспорт', state=Form_transport.country)
async def country_food(message: types.Message, state: FSMContext):
    translator = Translator(from_lang='ru', to_lang='en')
    async with state.proxy() as data:
        data['country'] = translator.translate(message.text)

    await Form_transport.next()
    await message.answer("Введите город:")


@db.callback_query_handler(state=Form_transport.city)
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
        button = 'Транспорт'

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
        gas = data['prices'][40]['avg']
        usd_gas = data['prices'][40]['usd']['avg']
        local_trans = data['prices'][42]['avg']
        usd_local_trans = data['prices'][42]['usd']['avg']
        taxi = data['prices'][43]['avg']
        usd_taxi = data['prices'][43]['usd']['avg']
        taxi_km = data['prices'][44]['avg']
        usd_taxi_km = data['prices'][44]['usd']['avg']
        taxi_start = data['prices'][45]['avg']
        usd_taxi_start = data['prices'][45]['usd']['avg']
        vw_golf = data['prices'][46]['avg']
        usd_vw_golf = data['prices'][46]['usd']['avg']

        await bot.send_message(message.chat.id,
                               f'Выбранная страна: {country}\nВыбранный город: {city}\n\U0001F4B2 Цены указаны в местной валюте ({currency}) и в долларах (USD)\n'
                               f'\nТранспорт\n'
                                   f'\U000026FD Топливо 1 л: {gas} {currency}, {usd_gas}$\n\U0001F68C Один проезд в общественном транспорте: {local_trans} {currency}; {usd_local_trans}$\n'
                                   f'\U0001F696 Такси, 1 час ожидания: {taxi} {currency}, {usd_taxi}$\n\U0001F695 Такси, за 1 км поездки: {taxi_km} {currency}; {usd_taxi_km}$\n\U0001F696 Подача такси (минимальная стоимость): {taxi_start} {currency}; {usd_taxi_start}$\n'
                                   f'\U0001F697 Покупка Volkswagen Golf 1.4 (или подобный новый автомобиль): {vw_golf} {currency}; {usd_vw_golf}$\n'
                                   )
    except:
        await bot.send_message(message.chat.id, '\U00002620 Проверьте данные')


def register_handlers_search(db: Dispatcher):
    db.register_message_handler(food_command, commands=['transport'])
    db.register_message_handler(country_food, state=Form_transport.country)
    db.register_message_handler(city_food, state=Form_transport.city)
