import flet as ft
import datetime
import calendar
from calendar import HTMLCalendar
from dateutil import relativedelta
from additionally import textColor, gradColor, allfonts, convert_date_calendar

# Класс Calendar наследуется от ft.UserControl
class Calendar(ft.UserControl):
    
    def __init__(self, page):
        super().__init__()

        # Создание кнопки "Принять" (apply_button) и установка обработчика события (on_click=self.button_clicked)
        self.apply_button = ft.ElevatedButton("Принять", on_click=self.button_clicked)
        self.page = page
        self.get_current_date()
        self.set_theme()
        self.click_count: list=[]
        self.apply_count: list=[]
        # Инициализация контейнера для календаря
        self.calendar_container = ft.Container(width=250, height=250,
                                          padding=ft.padding.all(2), 
                                          border=ft.border.all(2, self.border_color),
                                          border_radius=ft.border_radius.all(10),
                                          alignment=ft.alignment.bottom_center)
        self.build() # Построение календаря
        self.output = ft.Text() # Добавление элемента управления для вывода информации.
  
    def get_current_date(self):
        '''Получение текущей даты'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year 

    def set_current_date(self):
        '''Установка календаря на текущую дату.'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year 
        self.build()
        self.calendar_container.update()
        
    def get_next(self, e):
        '''Переход к следующему месяцу.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day) 
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month
        
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()
    
    def get_prev(self, e):
        '''Переход к предыдущему месяцу.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day) 
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def selected_date(self, e):
        '''Выбор пользователем даты'''
        self.click_count.append(e.control.data)
        if len(self.click_count) < 3:
            e.control.bgcolor = ft.colors.BLUE_600
        else:
            self.click_count: list=[]
            self.apply_count: list=[]
            self.build()
        e.control.update()
        self.update()
        
    def button_clicked(self, e):
        if len(self.click_count) == 2:
            print(convert_date_calendar(self.click_count[0], self.click_count[1]))
        if len(self.click_count) == 1:
            print(convert_date_calendar(self.click_count[0], self.click_count[0]))
        
    def get_calendar(self):
        '''Получение календаря из модуля calendar.'''
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)
    
    def set_theme(self, border_color=ft.colors.PINK_700, 
                  text_color="#352958", 
                  current_day_color=ft.colors.PINK_700):
        self.border_color = border_color
        self.text_color = text_color
        self.current_day_color = current_day_color
    
    def build(self):
        '''Построение календаря для flet.'''
        current_calendar = self.get_calendar()
        
        str_date = '{0} {1}, {2}'.format(calendar.month_name[self.current_month], self.current_day, self.current_year)
        
        date_display = ft.Text(str_date, text_align='center', size=16, color=self.text_color)
        next_button = ft.Container(ft.Text('>', text_align='right', size=16, color=self.text_color), on_click=self.get_next)
        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)
        prev_button = ft.Container(ft.Text('<', text_align='left', size=16, color=self.text_color), on_click=self.get_prev)
        
        calendar_column = ft.Column([ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY, 
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER, height=30, expand=False), div], 
                                    spacing=1, width=250, height=280, alignment=ft.MainAxisAlignment.START, expand=False)
        # Перебор недель и добавление строк.
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            # Перебор дней и добавление дней в строку.
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day)
                    if len(str(display_day)) == 1:
                        display_day = '0%s' % display_day
                    if day == self.current_day: 
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color
                        
                    day_button = ft.Container(content=ft.Text(str(display_day), weight=is_current_day_font, color=self.text_color), 
                                              on_click=self.selected_date, data=(self.current_month, day, self.current_year), 
                                              width=25, height=25, ink=True, alignment=ft.alignment.center,
                                              border_radius=ft.border_radius.all(10),
                                              bgcolor=is_current_day_bg)
                else:
                    day_button = ft.Container(width=25, height=25, border_radius=ft.border_radius.all(10))
                    
                week_row.controls.append(day_button)
                
            # Добавление недель в основную колонку.
            calendar_column.controls.append(week_row)
        # Добавление колонки в контейнер страницы. 
        calendar_column.controls.append(ft.Column([ft.Container(self.apply_button, alignment=ft.alignment.center, height=40), ft.Container()], spacing=2))
        self.calendar_container.content = calendar_column
        return self.calendar_container



# Класс Calendar представляет собой пользовательский календарь, созданный с помощью библиотеки flet. 
# Он позволяет пользователю выбрать даты и выводит информацию о выбранных датах после нажатия кнопки 
# "Принять". Календарь строится с использованием HTMLCalendar из модуля calendar и имеет кнопки для 
# перехода к предыдущему и следующему месяцам. Каждый день в календаре представлен в виде кнопки, 
# которую можно выбирать. Когда пользователь выбирает дату, кнопка подсвечивается, а информация о 
# выбранных датах сохраняется для последующего вывода.

# Важные методы включают build() для построения календаря, get_next() и get_prev() для перехода 
# к следующему и предыдущему месяцам соответственно, selected_date() для обработки выбора 
# пользователем даты, и button_clicked() для обработки нажатия кнопки "Принять".