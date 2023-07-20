import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import sqlite3
import matplotlib as mpl
from additionally import allfonts, textColor

def upload_data(beginDate, endDate):
    conn = sqlite3.connect("DataBase/ourDB.db")
    cursor = conn.cursor()
    PC = "PC"
    visPC = 0
    Smart = "Smartphones"
    visSmart = 0
    Table = "Tablets"
    visTable = 0
    cursor.execute('SELECT visits FROM Devices WHERE userDevice = ? AND date >= ? AND date <= ?', (PC, beginDate, endDate,))
    topa = list(cursor.fetchall())
    for i in topa:
        visPC += int(i[0])
    cursor.execute('SELECT visits FROM Devices WHERE userDevice = ? AND date >= ? AND date <= ?', (Smart, beginDate, endDate,))
    topa = list(cursor.fetchall())
    for i in topa:
        visSmart += int(i[0])
    cursor.execute('SELECT visits FROM Devices WHERE userDevice = ? AND date >= ? AND date <= ?', (Table, beginDate, endDate,))
    topa = list(cursor.fetchall())
    for i in topa:
        visTable += int(i[0])
    return visPC, visSmart, visTable

class Devices(ft.Container):
    def __init__(self, page: ft.Page, beginDate, endDate):
        super().__init__()
        self.page = page
        self.page.fonts = allfonts
        self.beginDate = beginDate
        self.endDate = endDate
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.update_chart()
        self.margin = ft.margin.only(left=30, top=6, bottom=10)
        self.border_radius = 10
        self.width = 277
        self.height = 467
        self.bgcolor = "white"
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Устройства посетителей",
                                    size=26,
                                    text_align="center",
                                    color=textColor,
                                    font_family="PantonBold",
                                    weight=200),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=15)
                ),
                ft.Container(
                    padding=-20,
                    content=MatplotlibChart(self.fig, expand=True),
                )
            ]
        )

    def update_chart(self):
        visPC, visSmart, visTable = upload_data(self.beginDate, self.endDate)
        labels = []
        sizes = []
        sizes.append(visPC)
        sizes.append(visSmart)
        sizes.append(visTable)
        labels.append('PC (' + str(visPC) + ')')
        labels.append('Смартфоны(' + str(visSmart) + ')')
        labels.append('Планшеты(' + str(visTable) + ')')
        self.ax.clear()  # Очистка предыдущих элементов
        patches, texts, autotexts = self.ax.pie(
            sizes,
            colors=['#9C91C9', '#6A54B9', '#503E8A'],
            textprops=dict(color='w', size=11),
            radius=1, autopct='%.0f%%', pctdistance=0.75
        )

        centre_circle = plt.Circle((0, 0), 0.5, color='white')
        self.ax.add_artist(centre_circle)
        self.ax.text(0, 0, 'Всего:\n' + str(sum(sizes)), ha='center', va='center', fontsize=11)
        mpl.rcParams['legend.fontsize']=8

        self.ax.set_aspect('equal')
        plt.tight_layout()

        legend = self.ax.legend(patches, labels,
                                loc="lower center", bbox_to_anchor=(0.5, -0.3), frameon=False, fancybox=True)
        self.fig.subplots_adjust(bottom=0.65)
        self.fig.set_size_inches(190 / 80, 477 / 80)  # Установка правильных размеров фигуры

    def renew(self):
        self.update_chart()
        self.page.update()