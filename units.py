import os
import matplotlib.pyplot as plt
from aiogram.types import InputFile
import pandas as pd
import uuid


def plot_1_day(temp, city):
    plt.figure()
    plt.bar(city, temp)
    plt.xlabel('Город')
    plt.ylabel('Температура')
    plt.title('Сравнение температуры')

    file_name = f'graph_1_day_{uuid.uuid4()}.jpg'
    plt.savefig(file_name)
    return file_name


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
