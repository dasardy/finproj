import sqlite3
import datetime
import pandas as pd
import flet as ft
from flet import *
import numpy as np
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import plotly.graph_objects as go
from additionally import allfonts, textColor

# Функция для загрузки данных из базы данных
def upload_data(beginDate, endDate):
    conn = sqlite3.connect('DataBase/ourDB.db')
    cursor = conn.cursor()
    # Запрос данных из базы данных для поисковых систем Yandex и Google
    cursor.execute('SELECT visits FROM SearchSystem WHERE searchsys = ? AND date >= ? AND date <= ? ORDER BY date ASC ',
                   ("Yandex", beginDate, endDate,))
    YaVisits = list(cursor.fetchall())
    cursor.execute('SELECT visits FROM SearchSystem WHERE searchsys = ? AND date >= ? AND date <= ? ORDER BY date ASC',
                   ("Google", beginDate, endDate,))
    GoVisits = list(cursor.fetchall())
    cursor.execute('SELECT date FROM SearchSystem WHERE searchsys = ? AND date >= ? AND date <= ? ORDER BY date ASC',
                   ("Yandex", beginDate, endDate,))
    dates = list(cursor.fetchall())
    dates_list = [i for i in dates]
    OtVisits = []
    # Запрос данных из базы данных для других поисковых систем
    for i in dates:
        cursor.execute('SELECT SUM (visits) FROM SearchSystem WHERE searchsys != "Yandex" AND searchsys != "Google" AND date = ?', (i[0],))
        OtVisits.append(list(cursor.fetchall()[0]))

    # Функция для конвертации даты в формат "дд.мм"
    def convert_date(date_str):
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m")
        return formatted_date

    # Функция для уплотнения списка данных
    def compress_list(input_list, merge_degree):
        compressed_list = []
        for i in range(0, len(input_list), merge_degree):
            sum_of_pairs = sum(input_list[i:i + merge_degree])
            compressed_list.append(sum_of_pairs)
        return compressed_list

    yandex_visits = []
    google_visits = []
    other_visits = []
    tickvals = []
    ticktext = []
    for i in range(len(dates_list)):
        yandex_visits.append(int(YaVisits[i][0]))
        google_visits.append(int(GoVisits[i][0]))
        if OtVisits[i][0] != None:
            other_visits.append(OtVisits[i][0])
        else:
            other_visits.append(0)

    scale = len(dates_list) // 11

    if scale != 0:
        yandex_visits1 = compress_list(yandex_visits, len(dates_list) // 11)
        google_visits1 = compress_list(google_visits, len(dates_list) // 11)
        other_visits1 = compress_list(other_visits, len(dates_list) // 11)
    else:
        yandex_visits1 = yandex_visits
        google_visits1 = google_visits
        other_visits1 = other_visits

    if scale != 0:
        for i in range(len(dates_list)):
            if i % scale == 0:
                ticktext.append(str(convert_date(dates_list[i][0])))
    else:
        for i in range(len(dates_list)):
            ticktext.append(str(convert_date(dates_list[i][0])))

    for i in range(len(ticktext)):
        tickvals.append(i)

    return yandex_visits1, google_visits1, other_visits1, tickvals, ticktext

# Класс-виджет
class SearchEngine(Container):
    def __init__(self, page: Page, beginDate, endDate):
        super().__init__()
        self.page = page
        self.page.fonts = allfonts
        self.beginDate = beginDate
        self.endDate = endDate
        self.fig = go.Figure()
        self.update_chart()
        self.margin = ft.margin.only(left=6, top=6, bottom=10, right=30)
        self.width = 630
        self.height = 467
        self.bgcolor = "white"
        self.border_radius = 10
        self.content = Column(
            controls=[
                Container(
                    content=Text("Посещаемость из поисковых систем",
                                  size=24,
                                  color=textColor,
                                  font_family="PantonBold"),
                    alignment=alignment.top_center,
                    margin=ft.margin.only(top=10),
                ),
                Container(
                    #width=700,
                    #height=240,
                    content=ft.plotly_chart.PlotlyChart(self.fig)
                )
            ]
        )

    # Обновление виджета
    def update_chart(self):
        self.fig.data = []
        yandex_visits1, google_visits1, other_visits1, tickvals, ticktext = upload_data(self.beginDate, self.endDate)
        self.fig.add_trace(go.Bar(y=yandex_visits1, name='Яндекс', marker=dict(color='#503E8A')))
        self.fig.add_trace(go.Bar(y=google_visits1, name='Google', marker=dict(color='#6B54BB')))
        self.fig.add_trace(go.Bar(y=other_visits1, name='Другие поисковые системы', marker=dict(color='#E43A6B')))
        self.fig.update_layout(
            barmode='stack',
            xaxis=dict(
                tickmode='array',
                tickvals=tickvals,
                ticktext=ticktext,
            ),
            margin=dict(
                l=40,  # отступ слева
                r=30,  # отступ справа
                b=150,  # отступ снизу
                t=0   # отступ сверху
            ),
            legend=dict(
                orientation='h',
                y=-0.1,
                x=0.5,
                xanchor='center',
                font=dict(
                    family='Panton-Regular',
                    size=16,
                    color='#352958'
                )
            ),
            plot_bgcolor="#FFFFFF",  # цвет фона сетки
            yaxis=dict(gridcolor="#E0E3FF"),  # цвет сетки оси Y
        )
    def renew(self):
        self.update_chart()
        self.page.update()



# Код загружает данные из базы данных и строит график с помощью plotly.graph_objects. 
# Класс SearchEngine наследуется от flet.Container и использует библиотеку flet для 
# создания контейнера с графиком и заголовком "Посещаемость из поисковых систем". 
# Метод update_chart обновляет данные графика на основе новых данных из базы данных. 
# Метод renew обновляет график и перерисовывает страницу.