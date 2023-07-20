import flet as ft
import datetime
import sqlite3
from additionally import allfonts, textColor

def upload_data(keyword_to_data, searchSys_to_data):
    today = datetime.date.today()
    first_day_of_month = today - datetime.timedelta(days=30)
    conn = sqlite3.connect('DataBase/ourDB.db')
    cursor = conn.cursor()
    # Выполнение SQL-запроса
    cursor.execute("SELECT position FROM positions WHERE keywords = ? AND search_engine = ? AND date >= ? ORDER BY date DESC",
                   (keyword_to_data, searchSys_to_data, first_day_of_month,))
    hit = list(cursor.fetchall())

    print(hit)

    total_positions = len(hit)
    top_10_count = len([position for position in hit if int(position[0]) <= 10])
    percent = (top_10_count / total_positions) * 100
    return percent

class Output(ft.Container):
    def __init__(self, keyword, searchSys, page: ft.Page):
        super().__init__()
        page.fonts = allfonts
        self.keyword = keyword
        self.searchSys = searchSys
        self.margin = ft.margin.only(top=6, left=6, right=30)
        self.chart = None  # Добавляем атрибут для хранения графика
        self.width = 257
        self.height = 250
        self.bgcolor = "white"
        self.border_radius = 10
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Процент вывода в топ 10",
                        size=24,
                        color=textColor,
                        text_align='center',
                        font_family="PantonBold"),
                    alignment=ft.alignment.top_center,
                    padding=10
                ),
                ft.Container(
                    content=self.update_chart(),
                    alignment=ft.alignment.center,
                    padding=-90)
            ]
        )

    def update_chart(self):
        percent = upload_data(self.keyword, self.searchSys)
        title = '0%' if percent == 0 else ''
        normal_radius = 17
        normal_title_style = ft.TextStyle(
            size=40, color=textColor, font_family="PantonBold"
        )
        # Обновляем существующий график, если он уже был создан ранее
        if self.chart is not None:
            self.chart.sections = [
                ft.PieChartSection(
                    100 - percent,
                    title=title,
                    title_style=normal_title_style,
                    title_position=-3.3,
                    color=ft.colors.WHITE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    percent,
                    title=str(round(percent)) + '%',
                    title_style=normal_title_style,
                    title_position=-3.3,
                    color="#6C53BB",
                    radius=normal_radius,
                ),
            ]
        else:
            # Если график еще не создан, создаем его
            self.chart = ft.PieChart(
                sections=[
                    ft.PieChartSection(
                        100 - percent,
                        title=title,
                        title_style=normal_title_style,
                        title_position=-3.3,
                        color=ft.colors.WHITE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        percent,
                        title=str(round(percent)) + '%',
                        title_style=normal_title_style,
                        title_position=-3.3,
                        color="#6C53BB",
                        radius=normal_radius,
                    ),
                ],
                sections_space=0,
                center_space_radius=55,
            )
        return self.chart  # Возвращаем сохраненный или созданный график

    def renew(self, keyword=None, searchSys=None):
        if searchSys is not None:
            self.searchSys = searchSys
        if keyword is not None:
            self.keyword = keyword
        self.update_chart()
        self.page.update()
