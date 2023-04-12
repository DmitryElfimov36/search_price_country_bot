import requests
import aiogram.utils.markdown as md
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from translate import Translator
from config import RAPID_API_KEY
from create_bot import db, bot
from data_base import sqlite_db


class Form_food(StatesGroup):
    country = State()
    city = State()


@db.callback_query_handler(text='food')
async def food_command(call: types.CallbackQuery):
    await Form_food.country.set()
    await call.message.answer('Введите страну:')


@db.callback_query_handler(text='Еда', state=Form_food.country)
async def country_food(message: types.Message, state: FSMContext):
    translator = Translator(from_lang='ru', to_lang='en')
    async with state.proxy() as data:
        data['country'] = translator.translate(message.text)

    await Form_food.next()
    await message.answer("Введите город:")


@db.callback_query_handler(state=Form_food.city)
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
        button = 'Еда'

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
        apples = data['prices'][7]['avg']
        usd_apples = data['prices'][7]['usd']['avg']
        banana = data['prices'][8]['avg']
        usd_banana = data['prices'][8]['usd']['avg']
        beef = data['prices'][9]['avg']
        usd_beef = data['prices'][9]['usd']['avg']
        wine = data['prices'][10]['avg']
        usd_wine = data['prices'][10]['usd']['avg']
        chick_br = data['prices'][11]['avg']
        usd_chick_br = data['prices'][11]['usd']['avg']
        beer = data['prices'][12]['avg']
        usd_beer = data['prices'][12]['usd']['avg']
        eggs = data['prices'][13]['avg']
        usd_eggs = data['prices'][13]['usd']['avg']
        white_bread = data['prices'][15]['avg']
        usd_white_bread = data['prices'][15]['usd']['avg']
        local_cheese = data['prices'][16]['avg']
        usd_cheese = data['prices'][16]['usd']['avg']
        milk = data['prices'][17]['avg']
        usd_milk = data['prices'][17]['usd']['avg']
        onion = data['prices'][18]['avg']
        usd_onion = data['prices'][18]['usd']['avg']
        oranges = data['prices'][19]['avg']
        usd_oranges = data['prices'][19]['usd']['avg']
        cigarettes = data['prices'][20]['avg']
        usd_cig = data['prices'][20]['usd']['avg']
        potato = data['prices'][21]['avg']
        usd_potato = data['prices'][21]['usd']['avg']
        rice = data['prices'][22]['avg']
        usd_rice = data['prices'][22]['usd']['avg']
        tomato = data['prices'][23]['avg']
        usd_tomato = data['prices'][23]['usd']['avg']
        water = data['prices'][24]['avg']
        usd_water = data['prices'][24]['usd']['avg']
        capp = data['prices'][29]['avg']
        usd_capp = data['prices'][29]['usd']['avg']
        cola = data['prices'][30]['avg']
        usd_cola = data['prices'][30]['usd']['avg']
        beer_cafe = data['prices'][31]['avg']
        usd_beer_cafe = data['prices'][31]['usd']['avg']
        imp_beer = data['prices'][32]['avg']
        usd_imp_beer = data['prices'][32]['usd']['avg']
        mc_combo = data['prices'][33]['avg']
        usd_mc_combo = data['prices'][33]['usd']['avg']
        meal_cafe = data['prices'][35]['avg']
        usd_meal_cafe = data['prices'][35]['usd']['avg']

        await bot.send_message(message.chat.id,
                               f'Выбранная страна: {country}\nВыбранный город: {city}\n\U0001F4B2 Цены указаны в местной валюте ({currency}) и в долларах (USD)\n'
                               f'\nПродукты питания\n\U0001F34E Яблоки, 1 кг: {apples} {currency}; {usd_apples}$\n\U0001F34C Бананы, 1 кг: {banana} {currency}; {usd_banana}$\n'
                               f'\U0001F969 Говяжье мясо, 1 кг: {beef} {currency}; {usd_beef}$\n\U0001F377 Бутылка вина: {wine} {currency}; {usd_wine}$\n\U0001F357 Куриная грудка: {chick_br} {currency}; {usd_chick_br}$\n'
                               f'\U0001F37A Пиво, 0.5 л: {beer} {currency}; {usd_beer}$\n\U0001F95A Яйца, 12 штук: {eggs} {currency}; {usd_eggs}$\n\U0001F35E Белый хлеб, 0.5 кг: {white_bread} {currency}; {usd_white_bread}$\n'
                               f'\U0001F9C0 Местный сыр, 1 кг: {local_cheese} {currency}; {usd_cheese}$\n\U0001F95B Молоко, 1 литр: {milk} {currency}; {usd_milk}$\n\U0001F9C5 Лук: {onion} {currency}; {usd_onion}$\n'
                               f'\U0001F34A Апельсины, 1 кг: {oranges} {currency}; {usd_oranges}$\n\U0001F6AC Пачка сигарет: {cigarettes} {currency}; {usd_cig}$\n\U0001F954 Картошка, 1 кг: {potato} {currency}; {usd_potato}$\n'
                               f'\U0001F35A Белый рис, 1 кг: {rice} {currency}; {usd_rice}$\n\U0001F345 Томаты: {tomato} {currency}; {usd_tomato}$\n\U0001F4A7 Вода, 1.5 л: {water} {currency}; {usd_water}$\n\n'
                               f'\nРестораны и кафе\n'
                               f'\U00002615 Капучино: {capp} {currency}; {usd_capp}$\n\U0001F964 Кока-кола, 0.33 л: {cola} {currency}; {usd_cola}$\n\U0001F37B Разливное пиво, 0.5 л: {beer_cafe} {currency}; {usd_beer_cafe}$\n'
                               f'\U0001F37A Импортное пиво, 0.33 л: {imp_beer} {currency}; {usd_imp_beer}$\n\U0001F354 \U0001F35F Комбо-набор Макдональдс: {mc_combo} {currency}; {usd_mc_combo}$\n'
                               f'\U0001F35D Питание в недорогом ресторане: {meal_cafe} {currency}; {usd_meal_cafe}$\n')
    except:
        await bot.send_message(message.chat.id, '\U00002620 Проверьте данные. Для повторного ввода выберите раздел'
                                                ' на клавиатуре выше')


def register_handlers_search(db: Dispatcher):
    db.register_message_handler(food_command, commands=['food'])
    db.register_message_handler(country_food, state=Form_food.country)
    db.register_message_handler(city_food, state=Form_food.city)
