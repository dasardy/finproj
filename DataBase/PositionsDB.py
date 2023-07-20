import sqlite3  # Импортируем модуль для работы с SQLite базой данных
from datetime import date  # Импортируем модуль для работы с датами
import requests  # Импортируем модуль для выполнения HTTP-запросов

def position_to_DB(TV_projectId, TV_token, TV_userId, start_date, end_date, con):
    projectId = TV_projectId  # ID вашего проекта

    headers = {
        'Content-Type': 'application/json',
        'User-Id': TV_userId,
        'Authorization': 'bearer ' + TV_token,
    }

    # Получение списка регионов проекта
    regions_indexes = []
    regionsSelectorData = {
        'id': projectId,
        'show_searchers_and_regions': 1
    }

    regionsSelector = requests.post('https://api.topvisor.com/v2/json/get/projects_2/projects', headers=headers, json=regionsSelectorData)
    regionsSelectorResult = regionsSelector.json().get('result')

    if regionsSelectorResult:
        project = regionsSelectorResult[0]
        for searcher in project['searchers']:
            for region in searcher['regions']:
                regions_indexes.append(region['index'])

    positionSelectorData = {
        'project_id': projectId,
        'regions_indexes': regions_indexes,
        'date1': start_date,
        'date2': end_date,
        'count_dates': 10,
        'show_exists_dates': 1,
        'show_headers': 1
    }

    positionsSelector = requests.post('https://api.topvisor.com/v2/json/get/positions_2/history', headers=headers, json=positionSelectorData)
    positionsSelectorResult = positionsSelector.json().get('result')

    if positionsSelectorResult:
        dates = positionsSelectorResult['headers']['dates']  # Получаем список дат из результатов
        projects = positionsSelectorResult['headers']['projects']  # Получаем список проектов из результатов
        keywords = positionsSelectorResult['keywords']  # Получаем список ключевых слов из результатов

        # Создание и подключение к базе данных SQLite
        conn = con
        cursor = conn.cursor()

        # Создание таблицы (если она не существует)
        cursor.execute('''CREATE TABLE IF NOT EXISTS positions
                        (keywords TEXT, search_engine TEXT, date DATE, position TEXT)''')

        for project in projects:
            for searcher in project['searchers']:
                for region in searcher['regions']:
                    # Запись информации о проекте, поисковике и регионе
                    for keyword in keywords:
                        # Запись ключевого слова, поисковой системы и позиций для каждой даты
                        for date in dates:
                            qualifiers = f"{date}:{project['id']}:{region['index']}"
                            if qualifiers in keyword['positionsData']:
                                positions = keyword['positionsData'][qualifiers]['position']
                                position_data = (keyword['name'], searcher['name'], date, positions) if positions else (keyword['name'], searcher['name'], date, '--')
                                cursor.execute("INSERT INTO positions VALUES (?, ?, ?, ?)", position_data)



# Этот код выполняет запросы к API сервиса Topvisor для получения данных о позициях по ключевым словам в поисковых системах. 
# Затем полученные данные записываются в базу данных SQLite, предполагая, что соединение с базой данных (con) уже 
# установлено перед вызовом этой функции. Код также создает таблицу positions, если она еще не существует, и записывает 
# данные в нее для каждой даты, проекта, поисковика и региона.