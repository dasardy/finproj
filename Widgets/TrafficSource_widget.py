import sqlite3
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from additionally import convert_date, textColor, allfonts
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.dates as mdates

# Функция для загрузки данных из базы данных
def upload_data(beginDate, endDate):
    # Создаем соединение с базой данных
    conn = sqlite3.connect("DataBase/ourDB.db")
    cursor = conn.cursor()

    DirTraf = 'Direct traffic'
    visDirTRaf = []
    dateAll =[]
    SearchEngine = 'Search engine traffic'
    visSearchEngine = []

    LinkTraf = 'Link traffic'
    visLinkTraf = []

    fresh_date = []
    # Запрос данных из базы данных для категории "Прямые переходы"
    cursor.execute('SELECT date, visits FROM TrafficSource WHERE traffic_source = ? AND date >= ? AND date <=?',
                   (DirTraf, beginDate, endDate,))
    topa = list(cursor.fetchall())

    for i in topa:
        visDirTRaf.append(i[1])
        fresh_date.append(i[0])
        dateAll.append(convert_date(i[0]))

    # Запрос данных из базы данных для категории "Поисковые системы"
    cursor.execute('SELECT visits FROM TrafficSource WHERE traffic_source = ? AND date >= ? AND date <= ?',
                   (SearchEngine, beginDate, endDate,))
    topa = list(cursor.fetchall())
    for i in topa:
        visSearchEngine.append(i[0])

    # Запрос данных из базы данных для категории "Переходы по ссылке"
    cursor.execute('SELECT visits FROM TrafficSource WHERE traffic_source = ? AND date >= ? AND date <= ?',
                   (LinkTraf, beginDate,  endDate,))
    topa = list(cursor.fetchall())
    for i in topa:
        visLinkTraf.append(i[0])
    return dateAll, visDirTRaf, visLinkTraf, visSearchEngine, fresh_date

# Класс-виджет
class TrafficSource(ft.Container):
    def __init__(self, page: ft.Page, beginDate, endDate):
        super().__init__()
        self.beginDate = beginDate
        self.endDate = endDate
        self.fig, self.ax = plt.subplots()
        self.update_chart()
        self.margin = ft.margin.only(left=6, top=6, right=30)
        self.border_radius = 10
        self.width = 632
        self.height = 448
        self.page = page
        self.bgcolor = "white"
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Источники трафика",
                                    size=26,
                                    text_align="center",
                                    color=textColor,
                                    font_family='PantonBold',
                                    weight=200),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=15)
                ),
                ft.Container(
                    content=MatplotlibChart(self.fig, expand=True,),
                ),
            ]
        )

    # Обновление виджета
    def update_chart(self):
        t, s, h, i, fdate = upload_data(self.beginDate, self.endDate)
        self.fig.data = []
        self.ax.clear()
        # Построение графика
        if len(t) == 1:
            self.ax.plot(fdate, s, label="Прямые переходы", color='#9C91C9', marker='o')
            self.ax.plot(fdate, h, label="Переходы по ссылке", color='#894F9C', marker='o')
            self.ax.plot(fdate, i, label="Поисковые системы", color='#C9426A', marker='o')
        else:
            self.ax.plot(fdate, s, label="Прямые переходы", color='#9C91C9')
            self.ax.plot(fdate, h, label="Переходы по ссылке", color='#894F9C')
            self.ax.plot(fdate, i, label="Поисковые системы", color='#C9426A')
        # Настройки графика
        self.ax.grid(color="grey", linewidth=0.2)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.set_facecolor('none')
        # Настройка меток оси X
        if len(fdate) > 11:
            if (len(fdate) % 11) != 0:
                step = int(len(fdate) / 11 + 1)
            else:
                step = int(len(fdate) / 11)
        else:
            step = 1
        to_set_t = fdate[::step]
        to_set_l = t[::step]
        self.ax.set_xticks(to_set_t)
        self.ax.set_xticklabels(to_set_l)
        self.fig.set_size_inches(545 / 80, 273 / 80)
        mpl.rcParams['legend.fontsize'] = 10
        legend = self.ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=3, frameon=False)
        plt.tight_layout()
        self.fig.set_tight_layout(True)

    def renew(self):
        self.update_chart()
        self.page.update()



# Код загружает данные из базы данных и строит график с помощью библиотеки matplotlib. 
# Класс TrafficSource наследуется от flet.Container и использует библиотеку flet для 
# создания контейнера с графиком и заголовком "Источники трафика". Метод update_chart 
# обновляет данные графика на основе новых данных из базы данных. Метод renew обновляет 
# график и перерисовывает страницу.