from additionally import allfonts, textColor
import sqlite3
import flet as ft
import datetime

def upload_data(keyword, searchSys):
    today = datetime.date.today()
    first_day_of_month = today - datetime.timedelta(days=30)
    conn = sqlite3.connect('DataBase/ourDB.db')
    cursor = conn.cursor()
    # Выполнение SQL-запроса
    cursor.execute('SELECT position FROM positions WHERE keywords = ? AND search_engine = ? ORDER BY date DESC',(keyword, searchSys,))
    lastUpdate = list(cursor.fetchone())[0]
    cursor.execute('SELECT position FROM positions WHERE keywords =  ? AND search_engine = ? AND date >= ? ORDER BY date ASC',(keyword, searchSys, first_day_of_month,))
    firstUpdate = list(cursor.fetchone())[0]
    conn.close()
    return lastUpdate, firstUpdate

class CurrPos(ft.Container):
    def __init__(self, keyword, searchSys, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.fonts = allfonts
        self.keyword = keyword
        self.searchSys = searchSys
        self.update_chart()
        self.margin = ft.margin.only(left=30, top=6)
        self.width=378
        self.height=250
        self.bgcolor="white"
        self.border_radius=10
    def update_chart(self):
        lastUpdate, firstUpdate = upload_data(self.keyword, self.searchSys)
        if int(lastUpdate) < int(firstUpdate):
            self.arrow = ft.Icon(name=ft.icons.ARROW_DROP_UP, color="green", size=150)
        elif int(lastUpdate) > int(firstUpdate):
            self.arrow = ft.Icon(name=ft.icons.ARROW_DROP_DOWN, color="red", size=150)
        else:
            self.arrow = ft.Icon(name=ft.icons.DRAG_HANDLE_ROUNDED, color="grey", size=150)
        self.pos = lastUpdate
        self.t="Ключевое слово: {} ".format(self.keyword) 

        if len(self.t)>34:
            self.t=self.t[:34]+"-\n"+self.t[34:]

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Позиция сайта", 
                                    color=textColor, 
                                    text_align='center', 
                                    size=26,
                                    font_family='PantonBold', 
                                    weight=40),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=5)),
                ft.Container(
                    content=ft.Row(
                        alignment = ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Container(
                                content=ft.Text(self.pos + "-е\nместо",
                                                size=37,
                                                color=textColor, 
                                                text_align='center', 
                                                font_family='PantonBold'),
                                ),
                            ft.Container(content=self.arrow, 
                                       )
                        ]
                    )
                ),
                ft.Container(
                    content=ft.Text(self.t, 
                                    size=18, 
                                    font_family="Panton",
                                    color=textColor,
                                    text_align='center'),
                    alignment=ft.alignment.top_center, padding=-20
                )
            ]
        )
    def renew(self, keyword=None, searchSys=None):
        if searchSys  is not None:
            self.searchSys = searchSys
        if keyword is not None:
            self.keyword = keyword
        self.update_chart()
        self.page.update()