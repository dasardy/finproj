import sqlite3  # Импортируем модуль для работы с SQLite базой данных
from tapi_yandex_metrika import YandexMetrikaStats  # Импортируем модуль для работы с API Яндекс.Метрики
from DataBase import DevicesDB, TrafficSourceDB, BrandTrafficDB, ConversionDB, SearchSystemDB, PositionsDB  # Импортируем функции для работы с базой данных и API
from datetime import date  # Импортируем модуль для работы с датами
import datetime  # Импортируем модуль для работы с датами и временем
import os  # Импортируем модуль для работы с файловой системой

# Параметры для доступа к API Яндекс.Метрики
METRIC_ACCESS_TOKEN = "y0_AgAAAABu9NRrAAog4AAAAADm7BmOrOpllZVrRHuLg0S7Sshfz-wVSCU"
METRIC_IDS = "12418261"
start_YM_date = '365daysAgo'
end_YM_date = 'today'

# Параметры для доступа к TopVizor
TV_projectId = 7784199
TV_token = '46d84eaa08c50379ce6b59607e0d5b79'
TV_userId = '358921'
start_TV_date = '2023-01-01'
end_TV_date = str(date.today())

def to_year():
    # Проверяем существует ли уже база данных, и если да, удаляем ее
    if os.path.exists("DataBase/ourDB.db"):
        os.remove("DataBase/ourDB.db")
        print("Удалена существующая база данных.")

    # Устанавливаем соединение с базой данных
    con = sqlite3.connect("DataBase/ourDB.db")
    cursor = con.cursor()

    # Создание таблиц для статистики по устройствам
    cursor.execute("""CREATE TABLE Devices
                    (date Text,  
                    userDevice TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по источникам трафика
    cursor.execute("""CREATE TABLE TrafficSource
                    (date Text,  
                    traffic_source TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по доле брендового и небрендового трафика
    cursor.execute("""CREATE TABLE BrandTraffic
                    (date integer,  
                    searchPhrase TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по конверсии
    cursor.execute("""CREATE TABLE Conversion
                    (date integer,  
                    goal TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по поисковым системам
    cursor.execute("""CREATE TABLE SearchSystem
                    (date integer,  
                    searchsys TEXT, 
                    visits INTEGER)
                """)

    # Загрузка данных во все таблицы
    DevicesDB.devices_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_YM_date, end_YM_date, con)
    TrafficSourceDB.TrafficSource_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_YM_date, end_YM_date, con)
    BrandTrafficDB.brand_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_YM_date, end_YM_date, con)
    ConversionDB.conversion_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_YM_date, end_YM_date, con)
    SearchSystemDB.search_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_YM_date, end_YM_date, con)
    PositionsDB.position_to_DB(TV_projectId, TV_token, TV_userId, start_TV_date, end_TV_date, con)

    con.commit()
    cursor.close()
    con.close()

def to_calendar(start_date, end_date):
    # Проверяем существует ли уже временная база данных, и если да, удаляем ее
    if os.path.exists("DataBase/temp.db"):
        os.remove("DataBase/temp.db")
        print("Удалена существующая временная база данных.")

    # Устанавливаем соединение с временной базой данных
    con2 = sqlite3.connect("DataBase/temp.db")
    cursor2 = con2.cursor()

    # Создание таблиц для статистики по устройствам
    cursor2.execute("""CREATE TABLE Devices
                (date Text,  
                userDevice TEXT, 
                visits INTEGER)
            """)

    # Создание таблиц для статистики по источникам трафика
    cursor2.execute("""CREATE TABLE TrafficSource
                    (date Text,  
                    traffic_source TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по доле брендового и небрендового трафика
    cursor2.execute("""CREATE TABLE BrandTraffic
                    (date integer,  
                    searchPhrase TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по конверсии
    cursor2.execute("""CREATE TABLE Conversion
                    (date integer,  
                    goal TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для для карты кликов
    cursor2.execute("""CREATE TABLE Clickmap
                    (date integer,  
                    URL TEXT, 
                    visits INTEGER)
                """)

    # Создание таблиц для статистики по поисковым системам
    cursor2.execute("""CREATE TABLE SearchSystem
                    (date integer,  
                    searchsys TEXT, 
                    visits INTEGER)
                """)

    # Загрузка данных во все таблицы, кроме топвизоровских
    DevicesDB.devices_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_date, end_date, con2)
    TrafficSourceDB.TrafficSource_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_date, end_date, con2)
    BrandTrafficDB.brand_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_date, end_date, con2)
    ConversionDB.conversion_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_date, end_date, con2)
    SearchSystemDB.search_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_date, end_date, con2)

    con2.commit()
    cursor2.close()
    con2.close()

    

# В этом коде определены две функции to_year() и to_calendar(start_date, end_date), которые создают 
# базы данных и загружают статистические данные в соответствующие таблицы. Параметры для работы с 
# API Яндекс.Метрики и TopVizor указаны в начале кода. Каждая функция выполняет следующие действия:

    # to_year(): Создает базу данных ourDB.db и создает таблицы для статистики по устройствам, источникам 
    # трафика, брендовому трафику, конверсии и поисковым системам. Затем загружает статистические данные 
    # в каждую таблицу с использованием соответствующих функций из DataBase.

    # to_calendar(start_date, end_date): Создает временную базу данных temp.db и создает таблицы для 
    # статистики по устройствам, источникам трафика, брендовому трафику, конверсии, карте кликов и поисковым 
    # системам. Затем загружает статистические данные в каждую таблицу с использованием соответствующих 
    # функций из DataBase.

# Код этих функций также обрабатывает удаление существующих баз данных, если они уже существуют перед созданием новых.