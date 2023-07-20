import matplotlib.pyplot as plt
import flet as ft
import sqlite3
import numpy as np
from additionally import allfonts, textColor
from flet.matplotlib_chart import MatplotlibChart

# Функция загрузки данных из базы данных для диаграммы
# Получает начальную и конечную дату в формате 'YYYY-MM-DD'
# Возвращает список меток и размеров для сегментов диаграммы
def upload_data(beginDate, endDate):
    conn = sqlite3.connect("DataBase/ourDB.db")
    cursor = conn.cursor()
    sizes = []
    col = 0
    labels = []

    # Получение уникальных поисковых запросов из таблицы BrandTraffic
    cursor.execute('SELECT DISTINCT searchPhrase FROM BrandTraffic WHERE searchPhrase != "" AND date >= ? AND date <= ? ORDER BY visits DESC', (beginDate, endDate,))
    topa = list(cursor.fetchall())

    for i in topa:
        length = len(str(i[0]))
        if length > 30:
            labels.append(str(i[0])[0:length - 30] + '-\n' + str(i[0])[length - 30:])
            length -= 30
        else:
            labels.append(str(i[0]))

        # Получение суммы визитов для каждого поискового запроса
        cursor.execute('SELECT SUM(visits) FROM BrandTraffic WHERE searchPhrase = ? AND date >= ? AND date <= ? ORDER BY SUM(visits) DESC', (i[0], beginDate, endDate,))
        topa = list(cursor.fetchall())
        for j in topa:
            sizes.append(int(j[0]))

    # Сортировка данных по убыванию размеров
    for i in range(len(labels) - 1):
        for j in range(len(labels) - 1):
            if sizes[j] < sizes[j + 1]:
                sizes[j], sizes[j + 1] = sizes[j + 1], sizes[j]
                labels[j], labels[j + 1] = labels[j + 1], labels[j]

    # Ограничение количества сегментов до 5 и создание меток вида "searchPhrase (visits)"
    sizes = sizes[:5]
    labels = labels[:5]
    for i in range(5):
        labels[i] += ' (' + str(sizes[i]) + ')'

    # Получение суммарного числа визитов для остальных поисковых запросов
    cursor.execute('SELECT SUM(visits) AS total FROM BrandTraffic  WHERE searchPhrase != "" AND date >= ? AND date <= ?', (beginDate, endDate,))
    topa = list(cursor.fetchall())
    for i in topa:
        col += int(i[0])
    col -= sum(sizes)
    sizes.append(col)
    labels.append('Остальное')
    
    # Закрытие соединения с базой данных и возврат данных
    cursor.close()
    conn.close()
    return labels, sizes

class BrandTraffic(ft.Container):
    def __init__(self, page: ft.Page, beginDate, endDate):
        # Конструктор класса BrandTraffic
        # Принимает объект страницы (page) из библиотеки flet, начальную и конечную даты
        super().__init__()
        self.beginDate = beginDate
        self.endDate = endDate
        self.page = page
        self.page.fonts = allfonts

        # Создание объекта Matplotlib для отрисовки диаграммы
        self.fig, self.ax = plt.subplots()

        # Вызов функции обновления диаграммы
        self.update_chart()

        # Установка параметров внешнего вида контейнера BrandTraffic
        self.margin = ft.margin.only(left=6, bottom=10, top=6)
        self.border_radius = 10
        self.width = 339
        self.height = 467
        self.bgcolor = "white"

        # Создание вертикальной колонки, в которую вложены элементы контейнера BrandTraffic
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Сегментация",
                        size=26,
                        text_align="center",
                        color=textColor,
                        font_family='PantonBold',
                        weight=200
                    ),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=15)
                ),
                ft.Container(
                    padding=-20,
                    content=MatplotlibChart(self.fig, expand=True,),
                )
            ]
        )
    
    # Функция обновления диаграммы
    def update_chart(self):
        labels = []
        sizes = []

        # Получение данных из базы данных с помощью функции upload_data
        labels, sizes = upload_data(self.beginDate, self.endDate)

        patches, texts = self.ax.pie(
            sizes,
            colors=['#ebe0f5', '#f8b5d2', '#e378a8','#a2d2ff','#a06ec4','#cba9ef','#ae60d3','#a2d2ff'],
            textprops=dict(color='#352958',size=6),
            radius=0.9
        )
        
        # Отображение подписей внутри диаграммы
        self.ax.set_aspect('equal')
        plt.tight_layout()
        plt.rcParams['legend.fontsize'] = 10
        legend = self.ax.legend(patches, labels,
            loc="lower center", bbox_to_anchor=(0.5,-0.65), frameon=False, fancybox=True)

        self.fig.subplots_adjust(bottom=0.5)
        self.fig.set_size_inches(339 / 80, 432 / 80)

    def renew(self):
        # Функция обновления диаграммы при изменении данных
        # Вызывает функцию update_chart и обновляет страницу (self.page)
        self.update_chart()
        self.page.update()



# BrandTraffic представляет собой кастомный контейнер из библиотеки flet, который 
# содержит диаграмму pie chart для отображения сегментации трафика по поисковым 
# запросам. Код содержит функции для загрузки данных из базы данных, обновления 
# диаграммы и обновления страницы при изменении данных.