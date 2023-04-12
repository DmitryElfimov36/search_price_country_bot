import requests
import aiogram.utils.markdown as md
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from translate import Translator
from config import RAPID_API_KEY
from create_bot import db, bot
from data_base import sqlite_db


class Form(StatesGroup):
    country = State()
    city = State()


# получение необходимых данных от пользователя
@db.callback_query_handler(text='all_data')
async def start_command(call_search: types.CallbackQuery):
    await Form.country.set()
    await call_search.message.answer('Введите страну:')


@db.callback_query_handler(text='Все данные', state=Form.country)
async def country(message: types.Message, state: FSMContext):
    translator = Translator(from_lang='ru', to_lang='en')
    async with state.proxy() as data:
        data['country'] = translator.translate(message.text)

    await Form.next()
    await message.answer("Введите город:")


# формирование структуры ответа
@db.callback_query_handler(state=Form.city)
async def city(message: types.Message, state: FSMContext):
    translator = Translator(from_lang='ru', to_lang='en')
    async with state.proxy() as data:
        data['city'] = translator.translate(message.text)
        await message.answer(
            md.text(
                md.text('Страна: ', md.bold(data['country'])),
                md.text('Город:', md.bold(data['city'])),
                sep='\n'
            ))
        # переменные для сохранения результата в БД
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        country = data['country']
        city = data['city']
        button = 'Все данные'

        await sqlite_db.db_table_val(us_id=us_id, user_id=us_name, country=country, city=city, button=button)
        await state.finish()

        # основной код ответа
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
            pair_of_jeans = data['prices'][4]['avg']
            usd_jeans = data['prices'][4]['usd']['avg']
            run_shoes = data['prices'][6]['avg']
            usd_shoes = data['prices'][6]['usd']['avg']
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
            rent_one_outside = data['prices'][25]['avg']
            usd_rent_one_outcide = data['prices'][25]['usd']['avg']
            rent_one_center = data['prices'][26]['avg']
            usd_rent_one_center = data['prices'][26]['usd']['avg']
            rent_three_outside = data['prices'][27]['avg']
            usd_rent_three_outside = data['prices'][27]['usd']['avg']
            rent_three_center = data['prices'][28]['avg']
            usd_rent_three_center = data['prices'][28]['usd']['avg']
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
            salary = data['prices'][36]['avg']
            usd_salary = data['prices'][36]['usd']['avg']
            ticket_cin = data['prices'][37]['avg']
            usd_ticket_cin = data['prices'][37]['usd']['avg']
            fit = data['prices'][38]['avg']
            usd_fit = data['prices'][38]['usd']['avg']
            tennis = data['prices'][39]['avg']
            usd_tennis = data['prices'][39]['usd']['avg']
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
            mobile = data['prices'][47]['avg']
            usd_mobile = data['prices'][47]['usd']['avg']
            utilities = data['prices'][48]['avg']
            usd_utilities = data['prices'][48]['usd']['avg']
            internet = data['prices'][49]['avg']
            usd_internet = data['prices'][49]['usd']['avg']
            mort = data['prices'][52]['avg']

            await bot.send_message(message.chat.id,
                                   f'Выбранная страна: {country}\nВыбранный город: {city}\n\U0001F4B2 Цены указаны в местной валюте ({currency}) и в долларах (USD)\n'
                                   f'\nПокупка жилья\n'
                                   f'\U0001F3E1 Стоимость покупки квартиры за пределами центра города (за 1 м²): \n'
                                   f'от {min_outside} {currency} до {max_outside} {currency};'
                                   f'\nот {usd_min_outside}$ до {usd_max_outside}$\n'
                                   f'\U0001F3E0 Стоимость покупки квартиры в центре города (за 1 м²): \n'
                                   f'от {min_center} {currency} до {max_center} {currency};\nот {usd_min_center}$ до {usd_max_center}$'
                                   f'\nОдежда и обувь\n\U0001F456 Пара джинс в сетевом магазине: {pair_of_jeans} {currency}; {usd_jeans}$\n'
                                   f'\U0001F45F Пара кроссовок: {run_shoes} {currency}; {usd_shoes}$\n'
                                   f'\nПродукты питания\n\U0001F34E Яблоки, 1 кг: {apples} {currency}; {usd_apples}$\n\U0001F34C Бананы, 1 кг: {banana} {currency}; {usd_banana}$\n'
                                   f'\U0001F969 Говяжье мясо, 1 кг: {beef} {currency}; {usd_beef}$\n\U0001F377 Бутылка вина: {wine} {currency}; {usd_wine}$\n\U0001F357 Куриная грудка: {chick_br} {currency}; {usd_chick_br}$\n'
                                   f'\U0001F37A Пиво, 0.5 л: {beer} {currency}; {usd_beer}$\n\U0001F95A Яйца, 12 штук: {eggs} {currency}; {usd_eggs}$\n\U0001F35E Белый хлеб, 0.5 кг: {white_bread} {currency}; {usd_white_bread}$\n'
                                   f'\U0001F9C0 Местный сыр, 1 кг: {local_cheese} {currency}; {usd_cheese}$\n\U0001F95B Молоко, 1 литр: {milk} {currency}; {usd_milk}$\n\U0001F9C5 Лук: {onion} {currency}; {usd_onion}$\n'
                                   f'\U0001F34A Апельсины, 1 кг: {oranges} {currency}; {usd_oranges}$\n\U0001F6AC Пачка сигарет: {cigarettes} {currency}; {usd_cig}$\n\U0001F954 Картошка, 1 кг: {potato} {currency}; {usd_potato}$\n'
                                   f'\U0001F35A Белый рис, 1 кг: {rice} {currency}; {usd_rice}$\n\U0001F345 Томаты: {tomato} {currency}; {usd_tomato}$\n\U0001F4A7 Вода, 1.5 л: {water} {currency}; {usd_water}$\n\n'
                                   f'\nАренда жилья\n'
                                   f'\U0001F3E1 Однокомнатная квартира за пределами центра города: {rent_one_outside} {currency}; {usd_rent_one_outcide}$\n'
                                   f'\U0001F3E2 Однокомнатная квартира в центре города: {rent_one_center} {currency}, {usd_rent_one_center}$\n'
                                   f'\U0001F3E1 Трехкомнатная квартира за пределами центра города: {rent_three_outside} {currency}; {usd_rent_three_outside}$\n'
                                   f'\U0001F3E2 Трехкомнатная квартира в центре города: {rent_three_center} {currency}; {usd_rent_three_center}$\n'
                                   f'\nРестораны и кафе\n'
                                   f'\U00002615 Капучино: {capp} {currency}; {usd_capp}$\n\U0001F964 Кока-кола, 0.33 л: {cola} {currency}; {usd_cola}$\n\U0001F37B Разливное пиво, 0.5 л: {beer_cafe} {currency}; {usd_beer_cafe}$\n'
                                   f'\U0001F37A Импортное пиво, 0.33 л: {imp_beer} {currency}; {usd_imp_beer}$\n\U0001F354 \U0001F35F Комбо-набор Макдональдс: {mc_combo} {currency}; {usd_mc_combo}$\n'
                                   f'\U0001F35D Питание в недорогом ресторане: {meal_cafe} {currency}; {usd_meal_cafe}$\n'
                                   f'\nЗарплата и финансы\n'
                                   f'\U0001F4B0 Средняя заработная плата после уплаты налогов: {salary} {currency}; {usd_salary}$\n'
                                   f'\nСпорт и досуг\n'
                                   f'\U0001F3A5 Билет в кино: {ticket_cin} {currency}; {usd_ticket_cin}$\n\U0001F3CB Фитнес и тренажерный зал: {fit} {currency} в месяц; {usd_fit}$ в месяц\n'
                                   f'\U0001F3BE Аренда теннисного корта в выходные, 1 час: {tennis} {currency}; {usd_tennis}$\n'
                                   f'\nТранспорт\n'
                                   f'\U000026FD Топливо 1 л: {gas} {currency}, {usd_gas}$\n\U0001F68C Один проезд в общественном транспорте: {local_trans} {currency}; {usd_local_trans}$\n'
                                   f'\U0001F696 Такси, 1 час ожидания: {taxi} {currency}, {usd_taxi}$\n\U0001F695 Такси, за 1 км поездки: {taxi_km} {currency}; {usd_taxi_km}$\n\U0001F696 Подача такси (минимальная стоимость): {taxi_start} {currency}; {usd_taxi_start}$\n'
                                   f'\U0001F697 Покупка Volkswagen Golf 1.4 (или подобный новый автомобиль): {vw_golf} {currency}; {usd_vw_golf}$\n'
                                   f'\n Коммунальные платежи, мобильная связь, интернет\n'
                                   f'\U0001F4F2 Минута разговора по телефону: {mobile} {currency}; {usd_mobile}$\n'
                                   f'\U0001F4B8 Основные коммунальные платежи для квартиры в 85 м² (электричество, вода, '
                                   f'отопление, вывоз мусора): {utilities} {currency}; {usd_utilities}$ (в среднем)\n '
                                   f'\U0001F310 Интернет: {internet} {currency}; {usd_internet}$ (в среднем)\n'
                                   f'\U0001F3E6 Процентная ставка по ипотеке на 20 лет: {mort}%')

        except:
            await bot.send_message(message.chat.id, '\U00002620 Проверьте данные')


def register_handlers_search(db: Dispatcher):
    db.register_message_handler(start_command, commands=['all_data'])
    db.register_message_handler(country, state=Form.country)
    db.register_message_handler(city, state=Form.city)
