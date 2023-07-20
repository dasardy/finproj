import flet as ft 
import sqlite3
from additionally import convert_date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from additionally import allfonts, textColor
from flet.matplotlib_chart import MatplotlibChart
import matplotlib as mpl

def upload_data(goal, beginDate, endDate):
    conn = sqlite3.connect('DataBase/ourDB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date FROM Conversion WHERE goal = ? AND date >= ? AND date <= ?', (goal, beginDate, endDate,))
    fresh_date = list(cursor.fetchall())
    dateAll = []
    goal_visits = []
    all_visits = []
    fdate = []
    for i in fresh_date:
        dateAll.append(convert_date(i[0]))
        fdate.append(i[0])
        cursor.execute('SELECT SUM(visits) FROM Conversion WHERE date = ?', (i[0],))
        all_visits.append(list(cursor.fetchone())[0])
        cursor.execute('SELECT visits FROM Conversion WHERE date=? AND goal =?', (i[0], goal,))
        goal_visits.append(list(cursor.fetchone())[0])
    conversion_on_date = []
    for i in range(len(dateAll)):
        conversion_on_date.append(goal_visits[i] / all_visits[i] * 100)
    return conversion_on_date, dateAll, goal_visits, fdate

class Conversion(ft.Container):
    def __init__(self, goal, page: ft.Page, beginDate, endDate):
        super().__init__()
        goals=[]
        conn = sqlite3.connect("DataBase/ourDB.db")
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT goal FROM Conversion WHERE goal != ""')
        topa = list(cursor.fetchall())
        for i in topa:
           goals.append(str(i[0]))

        self.goal = goal
        self.beginDate = beginDate
        self.endDate = endDate
        page.fonts = allfonts
        self.fig, self.ax1 = plt.subplots()
        self.ax2 = self.ax1.twinx()  # Создаем вторую ось y
        self.update_chart()
        self.margin = ft.margin.only(left=30, top=6)
        self.width = 632
        self.height = 448
        self.bgcolor = "white"
        self.border_radius = 10

        self.t=ft.Text(disabled=False,
            spans=[
                ft.TextSpan("{}". format(self.goal),
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))], size=18, font_family='Panton', color="#352958")
        self.ConversionBtn = ft.PopupMenuButton(
            items=[ft.PopupMenuItem(text=item,on_click=self.on_click) for item in goals],
            content=ft.Icon(name=ft.icons.INFO_ROUNDED, color="#9C91C9", size=32)
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Статистика по конверсии",
                                    size=26,
                                    font_family='PantonBold',
                                    text_align="center",
                                    color=textColor),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=10)
                ),
                ft.Container(
                    content=MatplotlibChart(self.fig, expand=True,),
                    padding=ft.padding.only(left=4)
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[ft.Container(width=120),self.ConversionBtn,
                        ft.Text("Цель:",size=18, 
                        font_family='Panton', color="#352958"),self.t],spacing=5),
                    alignment=ft.alignment.bottom_center
                )
            ]
        )

    def update_chart(self):
        self.fig.set_size_inches((527 / 80), (248 / 80))
        color = '#CDC0F0'
        conversion_rates, dates, target_visits, fdate = upload_data(self.goal, self.beginDate, self.endDate)
        self.ax1.clear()  # Очищаем график оси 1
        self.ax1.bar(fdate, target_visits, color=color, label="Целевые визиты")
        self.ax1.tick_params(axis='y', color="#352958")
        self.ax1.set_facecolor('none')
        if len(fdate)>11:
            if (len(fdate)%11)!=0:
                step = int(len(fdate)/11+1)
            else:
                step = int(len(fdate)/11)
        else:
            step = 1
        to_set_t = fdate[::step]
        to_set_l = dates[::step]
        self.ax1.set_xticklabels(to_set_l)
        self.ax1.set_xticks(to_set_t)
        ysticks2 = []
        for i in target_visits:
            ysticks2.append(i / 100)
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.spines['left'].set_visible(False)
        self.ax1.spines['bottom'].set_visible(False)

        color = '#DA2B5F'
        self.ax2.clear()  # Очищаем график оси 2
        self.ax2.set_yticklabels(ysticks2)
        if len(fdate)>50:
            self.ax2.plot(fdate, conversion_rates, color=color, label="Конверсия")
        else:
            self.ax2.plot(fdate, conversion_rates, color=color, marker='o', label="Конверсия")
        self.ax2.set_xticklabels(to_set_l)
        self.ax2.set_xticks(to_set_t)
        self.ax2.yaxis.set_major_formatter(mticker.PercentFormatter(symbol="%"))
        self.ax2.tick_params(axis='y', color="#352958")
        self.ax2.set_facecolor('none')
        self.ax2.spines['top'].set_visible(False)
        self.ax2.spines['right'].set_visible(False)
        self.ax2.spines['left'].set_visible(False)
        self.ax2.spines['bottom'].set_visible(False)

        mpl.rcParams['legend.fontsize'] = 10
        legend1 = self.ax1.legend(loc='lower center', bbox_to_anchor=(0.4, -0.3), frameon=False)
        legend2 = self.ax2.legend(loc='lower center', bbox_to_anchor=(0.7, -0.3), frameon=False)
        self.fig.subplots_adjust(bottom=0.2)
        self.fig.tight_layout()

    def renew(self):
        self.update_chart()
        self.page.update()
    
    def on_click(self,e):
        self.goal=e.control.text
        self.t=ft.Text(disabled=False,
        spans=[
            ft.TextSpan("{}". format(self.goal),
                ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))], size=18, font_family='Panton', color="#352958")
        
        self.t.update()
        print(self.goal)
        self.update()
