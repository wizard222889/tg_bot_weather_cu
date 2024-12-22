<<<<<<< HEAD
import matplotlib.pyplot as plt
from aiogram import Bot
import os
import pandas as pd
import requests
import uuid

#с помощью matplotlib построим график для 1 дня
=======
import os
import matplotlib.pyplot as plt
from aiogram.types import InputFile
import pandas as pd
import uuid


>>>>>>> origin/main
def plot_1_day(temp, city):
    plt.figure()
    plt.bar(city, temp)
    plt.xlabel('Город')
    plt.ylabel('Температура')
    plt.title('Сравнение температуры')

    file_name = f'graph_1_day_{uuid.uuid4()}.jpg'
    plt.savefig(file_name)
    return file_name

<<<<<<< HEAD
#с помощью matplotlib построим график для 5 дней
=======

>>>>>>> origin/main
def plot_5_day(city_temp):
    data_weather = []
    for city, weather in city_temp.items():
        for date, temp in weather:
            data_weather.append({'Город': city, 'Дата': date, 'Температура': temp})
    df = pd.DataFrame(data_weather)

    plt.figure(figsize=(10, 6))
    for city in df['Город'].unique():
        df_city = df[df['Город'] == city]
        plt.plot(df_city['Дата'], df_city['Температура'], marker='o', label=city)
    plt.title('Сравнение температуры')
    plt.xlabel('День')
    plt.ylabel('Температура (°C)')
    plt.grid()
    plt.legend()

    file_name = f'graph_5_day_{uuid.uuid4()}.jpg'
    plt.savefig(file_name)
    return file_name
<<<<<<< HEAD

#обработчки ошибок(в частности направлен на работу с api погоды, в обычных ошибках будет подробности выдавать)
async def send_error_message(chat_id, bot: Bot, exception: Exception):
    print()
    error_message = 'Ошибка'
    if isinstance(exception, requests.exceptions.ConnectionError):
        error_message = "Ошибка подключения: не удалось подключиться к серверу."
    elif isinstance(exception, requests.exceptions.HTTPError):
        error_message = f"Ошибка API: {exception.response.status_code}"
    elif isinstance(exception, ValueError):
        error_message = "Неправильные данные, попробуйте позже."
    elif isinstance(exception, PermissionError):
        error_message = "API не работают или доступ запрещен."
    else:
        error_message = f"Произошла непредвиденная ошибка, повторите позже. Подробности: {str(exception)}"
    await bot.send_message(chat_id, error_message)
=======
>>>>>>> origin/main
