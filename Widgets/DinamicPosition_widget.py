import sqlite3
import datetime
import pandas as pd
import flet as ft
import numpy as np
import plotly.express as px
from flet.plotly_chart import PlotlyChart
from additionally import allfonts, textColor

# Функция для увеличения дней при смене месяца
def increase_days_on_month_change(days_list):
    result = [days_list[0]]  # Копируем первый элемент, он не будет изменен
    for i in range(1, len(days_list)):
        current_day = days_list[i]
        previous_day = result[i - 1]  # Используем результат, а не исходный список
        if current_day < previous_day:
            current_day += 31
        result.append(current_day)
    return result

# Функция для конвертации даты в формат "дд.мм"
def convert_date(date_str):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d.%m")
    return formatted_date

# Функция для загрузки данных из базы данных
def upload_data(keyword_to_data, searchSys_to_data):
    conn = sqlite3.connect('DataBase/ourDB.db')
    cursor = conn.cursor()
    endDate = datetime.date.today()
    beginDate = datetime.date(endDate.year, endDate.month - 1, endDate.day)

    # Запрос данных из базы данных
    cursor.execute('SELECT date FROM positions WHERE keywords = ? AND search_engine= ? AND date > ? ORDER BY date ASC',
                   (keyword_to_data, searchSys_to_data, beginDate))
    dates = cursor.fetchall()
    dates_list = [list(date) for date in dates]

    cursor.execute('SELECT position FROM positions WHERE keywords = ? AND search_engine= ? AND date > ? ORDER BY date ASC',
                   (keyword_to_data, searchSys_to_data, beginDate))
    positions = cursor.fetchall()

    # Обработка данных для импользования графиком
    days = []
    months = []
    ticktext = []
    i = 0
    for date in dates_list:
        day = int(date[0].split('-')[2])
        month = int(date[0].split('-')[1])
        months.append(month)
        days.append(day)
        if days[i] - days[i-1] != -1:
            ticktext.append(str(convert_date(dates_list[i][0])))
        else:
            ticktext.append("")
        i += 1
    loops = months[-1] - months[0]
    for i in range(loops):
        days = increase_days_on_month_change(days)
    return days, positions, ticktext

    # Отрисовка графика
class Dinamics(ft.Container):
    def __init__(self, keyword, searchSys, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.fonts = allfonts
        self.keyword = keyword
        self.searchSys = searchSys
        self.fig = px.line()
        self.update_chart()
        self.margin = ft.margin.only(left=6, top=6)
        self.width = 613
        self.height = 249
        self.bgcolor = "white"
        self.border_radius = 10
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Динамика позиций", size=24, color=textColor, weight=ft.FontWeight.W_500,
                                    font_family="PantonBold"),
                    alignment=ft.alignment.top_center,
                    margin=ft.margin.only(top=10),
                ),
                ft.Container(
                    padding=ft.padding.only(top=-10),
                    content=ft.plotly_chart.PlotlyChart(self.fig)
                )
            ]
        )
    def update_chart(self):
        self.fig.data=[]
        days, positions, ticktext = upload_data(self.keyword, self.searchSys)
        xAxis = np.array(days)  
        yAxis = np.array([int(position[0]) for position in positions])
        df = pd.DataFrame(dict(
            x=xAxis,
            y=yAxis
        ))
        self.fig = px.line(df, x="x", y="y")
        self.fig.update_xaxes(title_text=None, range=[min(xAxis) - 1, max(xAxis) + 1],
                         tickfont=dict(family="Panton-Regular", size=11, color=textColor),
                         tickvals=xAxis, ticktext=ticktext, tickmode='array')
        self.fig.update_yaxes(title_text=None, range=[max(yAxis) + 1, 0],
                         tickfont=dict(family="Panton-Regular", size=11, color=textColor))
        self.fig.update_layout(
            height=220,
            margin=dict(
                l=30,  # отступ слева
                r=30,  # отступ справа
                b=30,  # отступ снизу
                t=0   # отступ сверху
            ),
            plot_bgcolor="#FFFFFF",  # цвет фона сетки
            xaxis=dict(gridcolor="#E0E3FF"),  # цвет сетки оси X
            yaxis=dict(gridcolor="#E0E3FF"),  # цвет сетки оси Y
        )
        self.fig.update_traces(line_color="#F23B67", line_shape="spline", line_smoothing=0.6)
    def renew(self, keyword = None, searchSys=None):
        if searchSys!=None:
            self.searchSys=searchSys
        if keyword!=None:
            self.keyword =keyword
        self.update_chart()
        self.page.update

# Код загружает данные из базы данных, строит график с помощью plotly.express, а затем 
# использует библиотеку flet для создания контейнера с этим графиком и заголовком "Динамика позиций". 
# Класс Dinamics отображает график и формирует внешний вид контейнера.