from tapi_yandex_metrika import YandexMetrikaStats  # Импортируем модуль для работы с API Яндекс.Метрики
import sqlite3  # Импортируем модуль для работы с SQLite базой данных

def brand_to_DB(METRIC_ACCESS_TOKEN, METRIC_IDS, start_date, end_date, con):
    # Создаем объект для работы с API Яндекс.Метрики
    api = YandexMetrikaStats(
        access_token=METRIC_ACCESS_TOKEN,
        receive_all_data=True
    )

    # Параметры запроса к API
    params = {
        'ids': METRIC_IDS,
        'metrics': 'ym:s:visits',  # Измеряем метрику "количество визитов"
        'dimensions': 'ym:s:date, ym:s:<attribution>SearchPhrase',  # Группируем данные по дате и поисковым фразам
        'date1': start_date,
        'date2': end_date,
        'sort': 'ym:s:date',
        'accuracy': 'full',
        'limit': 100000
    }

    # Получаем данные из API Яндекс.Метрики
    result = api.stats().get(params=params)
    result = result().data
    result = result[0]['data']

    # Создаем объект курсора для выполнения SQL-запросов
    cursor = con.cursor()

    # Обрабатываем полученные данные и вставляем их в базу данных
    for i in range(len(result)):
        date = result[i]['dimensions'][0]['name']  # Получаем дату измерения
        searchPhrase = result[i]['dimensions'][1]['name']  # Получаем поисковую фразу
        visits = result[i]['metrics'][0]  # Получаем количество визитов

        # Выполняем SQL-запрос на вставку данных в таблицу BrandTraffic
        cursor.execute('''
            INSERT INTO BrandTraffic (date, searchPhrase, visits)
            VALUES (?, ?, ?)
        ''', (date, searchPhrase, visits))



# В данном коде используется API Яндекс.Метрики для получения данных о посещениях сайта, 
# связанных с поисковыми фразами, которые являются брендовыми запросами. Затем полученные 
# данные записываются в базу данных SQLite, предполагая, что соединение с базой данных (con) 
# уже установлено перед вызовом этой функции. Каждая запись в базе данных содержит дату 
# измерения, брендовую поисковую фразу и количество визитов, связанных с этой фразой.