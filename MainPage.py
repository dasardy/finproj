from additionally import textColor, gradColor, allfonts, convert_date_calendar
import sqlite3
import calendar
import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import datetime
from functools import partial
from TopButtons import *
from Widgets.CurrentPositions_widget import CurrPos
from Widgets.DinamicPosition_widget import Dinamics
from Widgets.OutputPercent_widget import Output
from Widgets.Conversion_widget import Conversion
from Widgets.TrafficSource_widget import TrafficSource
from Widgets.Devices_widget import Devices
from Widgets.BrandTraff_widget import BrandTraffic
from Widgets.SearchEngine_widget import SearchEngine
from Widgets.Calendar_widget import Calendar
import DataBase.ALLDATA as AD

beginDate = datetime.date.today() - datetime.timedelta(days=30)
endDate= datetime.date.today()

conn = sqlite3.connect("DataBase/ourDB.db")
cursor = conn.cursor()
search=["Yandex","Google"]
keywords=[]
cursor.execute('SELECT DISTINCT keywords FROM positions')
topa = list(cursor.fetchall())
for i in topa:
    keywords.append(str(i[0]))
cursor.close()
conn.close()



def main(page: ft.Page):
    #INITIALIZATION OF COMPONENTS
    DP = Dinamics("газобетон", "Yandex", page)
    CP = CurrPos("газобетон", "Yandex", page)
    BT = BrandTraffic(page, beginDate, endDate)
    SS = SearchEngine(page, beginDate, endDate)
    TrafS = TrafficSource(page, beginDate, endDate)
    Devs = Devices(page, beginDate, endDate)
    Conv =  Conversion('Нажатие "Заказать звонок"', page, beginDate, endDate)
    def click_change_keyword(e):
        CP.renew(keyword=e.control.text)
        DP.renew(keyword=e.control.text)
    def click_change_ss(e):
        CP.renew(searchSys=e.control.text)
        DP.renew(searchSys=e.control.text)

    KeywordBtn = ft.PopupMenuButton(
        items=[ft.PopupMenuItem(text=item,on_click=click_change_keyword) for item in keywords],
        content=ft.Icon(name=ft.icons.MENU_BOOK_ROUNDED, color=textColor, size=26)
    )
    SearchBtn = ft.PopupMenuButton(
        items=[ft.PopupMenuItem(text=item,on_click=click_change_ss) for item in search],
        content=ft.Icon(name=ft.icons.SEARCH, color=textColor, size=26)
    )
    CalendarBtn = ft.PopupMenuButton(
        items=[
           ft.Container(Calendar(page)),
        ],content=ft.Row(
                    controls=[
                        ft.Container(),
                        ft.Icon(name=ft.icons.CALENDAR_MONTH_ROUNDED, color=textColor, size=26),
                        ft.Text(str(datetime.datetime.today().day)+' '
                                +str(calendar.month_name[datetime.datetime.today().month])+' '
                                +str(datetime.datetime.today().year),
                                font_family='PantonBold',
                                text_align="center",
                                color=textColor)
                       
                    ],spacing=5
        )
    )
    
    def on(e, BtnName):
        if BtnName=="Сегодня":
            new_bdate = datetime.date.today()
            new_edate = datetime.date.today()
        elif BtnName=="Вчера":
            new_bdate = datetime.date.today() - datetime.timedelta(days=1)
            new_edate = datetime.date.today()
        elif BtnName=="Неделя":
            new_bdate = datetime.date.today() - datetime.timedelta(days=7)
            new_edate = datetime.date.today()
        elif BtnName=="Месяц":
            new_bdate = datetime.date.today() - datetime.timedelta(days=30)
            new_edate = datetime.date.today()
        elif BtnName=="Квартал":
            new_bdate = datetime.date.today() - datetime.timedelta(days=91)
            new_edate = datetime.date.today()
        else:
            new_bdate = datetime.date.today() - datetime.timedelta(days=365)
            new_edate = datetime.date.today()
        Conv.beginDate = new_bdate
        TrafS.beginDate = new_bdate
        Devs.beginDate = new_bdate
        BT.beginDate = new_bdate
        SS.beginDate = new_bdate

        Conv.endDate = new_edate
        TrafS.endDate = new_edate
        Devs.endDate = new_edate
        BT.endDate = new_edate
        SS.endDate = new_edate
        
        Conv.renew()
        TrafS.renew()
        Devs.renew()
        BT.renew()
        SS.renew()


    TodayBtn = TopButton("Сегодня", 164, page, on_click=lambda e: on(e, TodayBtn.text))
    YestBtn = TopButton("Вчера", 157, page, on_click=lambda e: on(e, YestBtn.text))
    WeekBtn = TopButton("Неделя", 170, page, on_click=lambda e: on(e, WeekBtn.text))
    MonBtn = TopButton("Месяц", 158, page, on_click=lambda e: on(e, MonBtn.text))
    QuadButn =TopButton("Квартал", 175, page, on_click=lambda e: on(e, QuadButn.text))
    YearBtn = TopButton("Год", 130, page, on_click=lambda e: on(e, YearBtn.text))
    page.fonts = allfonts
    Dashboard = ft.Container(
        margin=0,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=gradColor
        ),
        border_radius=10,
        content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("SEO Дашборд",
                        size=30,
                        color="white", 
                        font_family="PantonBold"),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=5)
                ),
                ft.Container(
                    content=  ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            TodayBtn,YestBtn,WeekBtn, MonBtn, QuadButn, YearBtn,ft.Container(width=81),
                            ft.Container(CalendarBtn,bgcolor='white',border_radius=10,width=144,height=30),
                            ft.Container(width=15),ft.Container(KeywordBtn,bgcolor='white',border_radius=10,width=30,height=30),
                            ft.Container(width=3),ft.Container(SearchBtn,bgcolor='white',border_radius=10,width=30,height=30,margin=ft.margin.only(right=30))
                        ],
                        spacing=2
                    ),
                    padding= ft.padding.only(left=30)
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        CP, DP,
                        Output("газобетон", "Yandex", page)
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        Conv,
                        TrafS
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        Devs,BT,SS
                    ]
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    )
    page.add(Dashboard)
ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0",port=5002)
