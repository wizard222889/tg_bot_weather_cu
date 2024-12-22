from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from states import *
from weather_class import Weather
from units import *
import asyncio

api_token = '7667666842:AAE3o_4zjg9sbyIeAmhumyVGdhszb3sK1mQ'
api_key_weather = '7YjjQmVyCyeTYPc1PULYvntySIEqkG69'

bot = Bot(token=api_token)
dp = Dispatcher()

user_states = {}
city_temp = {}


@dp.message(F.text == '/start')
async def echo(message: types.Message):
    button_about = KeyboardButton(text='О боте')
    button_inline = KeyboardButton(text='Инлайн-кнопки')

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_about], [button_inline]],
        resize_keyboard=True
    )

    await message.answer(
        'Привет! Я бот прогноз погоды. Выберите действие с помощью кнопок ниже или отправьте команду /help.',
        reply_markup=reply_keyboard,
    )


@dp.message(F.text == '/help')
async def help(message: types.Message):
    await message.answer('Команда /start - стартовое сообщение и краткая информация\n'
                         'Команда /weather - прогноз погоды по начальной и конечной точки, также есть возможность вписать дополнительные города')


@dp.message(F.text == '/weather')
async def weather_start_city(message: types.Message, state: FSMContext):
    user_states[message.from_user.id] = []
    await state.set_state(Form.first_city)
    await message.answer(f'Введите начальный город: ')


@dp.message(F.text, Form.first_city)
async def weather_end_city(message: types.Message, state: FSMContext):
    user_states[message.from_user.id] = [message.text]
    await message.answer(f'Введи конечный город: ')
    await state.set_state(Form.end_city)


@dp.message(F.text, Form.end_city)
async def weather_add_city(message: types.Message, state: FSMContext):
    user_states[message.from_user.id].append(message.text)
    button_yes = InlineKeyboardButton(text='Да', callback_data='yes')
    button_no = InlineKeyboardButton(text='Нет', callback_data='no')
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_yes], [button_no]]
    )
    await state.clear()
    await message.answer('Еще будут города?', reply_markup=inline_keyboard)


@dp.callback_query(F.data == 'yes')
async def additional_cities_on(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Form.additional_cities)
    await callback.message.answer('Впишитие город: ')


@dp.message(F.text, Form.additional_cities)
async def additional_cities_off(message: types.Message):
    user_states[message.from_user.id].append(message.text)
    button_yes = InlineKeyboardButton(text='Да', callback_data='yes')
    button_no = InlineKeyboardButton(text='Нет', callback_data='no')
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_yes], [button_no]]
    )
    await message.answer('Еще будут города?', reply_markup=inline_keyboard)


@dp.callback_query(F.data == 'no')
async def get_weather(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    button_1_day = InlineKeyboardButton(text='1 день', callback_data='1_day')
    button_5_day = InlineKeyboardButton(text='5 дней', callback_data='5_day')
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1_day], [button_5_day]]
    )
    await callback.message.answer('Какой промежуток времени брать?', reply_markup=inline_keyboard)
    await state.clear()


@dp.callback_query(F.data == '1_day')
async def weather_1_day(callback: types.CallbackQuery):
    await callback.answer()
    text = ''
    weather = Weather(api_key=api_key_weather)
    for city in user_states[callback.from_user.id]:
        city_code = weather.get_city_code(city)
        weather_city = weather.get_weather(city_code, '1day')
        temp = f'Температура: {weather_city["temp"]}°C'
        humidity = f'Влажность: {weather_city["humidity"]}%'
        speed_wind = f'Скорость ветра: {weather_city["speed_wind"]}км/ч'
        probability = f'Вероятность дождя: {weather_city["probability"]}%'
        analysis = weather.weather_detection(weather_city['temp'], weather_city['humidity'],
                                             weather_city['speed_wind'], weather_city['probability'])
        description = '. '.join(analysis[:-1])
        level = analysis[-1]
        city_temp[city] = weather_city['temp']
        text += f'Погода для города {city} на {weather_city["date"]}\n\n' + temp + '\n' + humidity + '\n' + speed_wind + '\n' + probability + '\n' + f'Анализ погоды: {description}' + '\n' + f'Уровень погоды: {level}\n\n'
    await callback.message.answer(text)

    button_graph_yes = InlineKeyboardButton(text='Да', callback_data='yes_graph_1_day')
    button_graph_no = InlineKeyboardButton(text='Нет', callback_data='no_graph')
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_graph_yes], [button_graph_no]]
    )
    await callback.message.answer('Показать график для температуры?', reply_markup=inline_keyboard)


@dp.callback_query(F.data == '5_day')
async def weather_1_day(callback: types.CallbackQuery):
    await callback.answer()
    text = ''
    weather = Weather(api_key=api_key_weather)
    for city in user_states[callback.from_user.id]:
        city_code = weather.get_city_code(city)
        city_temp[city] = []
        weather_city = weather.get_weather(city_code, '5day')
        for day in weather_city:
            temp = f'Температура: {day["temp"]}°C'
            humidity = f'Влажность: {day["humidity"]}%'
            speed_wind = f'Скорость ветра: {day["speed_wind"]}км/ч'
            probability = f'Вероятность дождя: {day["probability"]}%'
            analysis = weather.weather_detection(day['temp'], day['humidity'],
                                                 day['speed_wind'], day['probability'])
            description = '. '.join(analysis[:-1])
            level = analysis[-1]
            city_temp[city].append((day['date'], day['temp']))
            text += f'Погода для города {city} на {day["date"]}\n\n' + temp + '\n' + humidity + '\n' + speed_wind + '\n' + probability + '\n' + f'Анализ погоды: {description}' + '\n' + f'Уровень погоды: {level}\n\n'
    await callback.message.answer(text)

    button_graph_yes = InlineKeyboardButton(text='Да', callback_data='yes_graph_5_day')
    button_graph_no = InlineKeyboardButton(text='Нет', callback_data='no_graph')
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_graph_yes], [button_graph_no]]
    )
    await callback.message.answer('Показать график для температуры?', reply_markup=inline_keyboard)


@dp.callback_query(F.data == 'no_graph')
async def goodbye_user(callback: types.CallbackQuery):
    user_states[callback.from_user.id] = []
    await callback.message.answer('Всего доброго! Если хотите еще раз попробовать, напишите команду /weather')


@dp.callback_query(F.data == 'yes_graph_5_day')
async def create_graph_5_day(callback: types.CallbackQuery):
    await callback.answer()
    file_name = plot_5_day(city_temp=city_temp)
    photo_file = FSInputFile(path=file_name)
    await bot.send_photo(chat_id=callback.message.chat.id, photo=photo_file)
    os.remove(file_name)


@dp.callback_query(F.data == 'yes_graph_1_day')
async def create_graph_1_day(callback: types.CallbackQuery):
    await callback.answer()
    file_name = plot_1_day(city_temp.values(),
                           city_temp.keys())
    photo_file = FSInputFile(path=file_name)
    await bot.send_photo(chat_id=callback.message.chat.id, photo=photo_file)
    os.remove(file_name)


@dp.message()
async def handle_unrecognized_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос. Попробуйте использовать команды или кнопки.')


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)


    asyncio.run(main())
