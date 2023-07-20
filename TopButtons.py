from additionally import textColor, allfonts  # Импортируем константы textColor и allfonts из модуля additionally
import flet as ft  # Импортируем модуль flet и называем его псевдонимом ft

class TopButton(ft.ElevatedButton):
    def __init__(self, btn_text, width, page: ft.Page, on_click=None):
        super().__init__()  # Вызываем конструктор родительского класса ft.ElevatedButton

        page.fonts = allfonts  # Устанавливаем все шрифты для страницы, используя константу allfonts

        self.text = btn_text  # Устанавливаем текст кнопки, переданный в аргументе btn_text
        self.width = width  # Устанавливаем ширину кнопки, переданную в аргументе width
        self.color = textColor  # Устанавливаем цвет текста кнопки, используя константу textColor
        self.height = 30  # Устанавливаем высоту кнопки (по умолчанию 30)
        self.bgcolor = "white"  # Устанавливаем цвет фона кнопки (по умолчанию белый)
        
        # Устанавливаем стиль кнопки, используя ft.ButtonStyle, указываем форму с закругленными углами (RoundedRectangleBorder)
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )

        self.on_click = on_click  # Устанавливаем функцию, которая будет вызвана при клике на кнопку (переданную в аргументе on_click)



# Этот код определяет класс TopButton, который является наследником класса ft.ElevatedButton из модуля flet. 
# Класс представляет собой кастомную кнопку с дополнительными настройками внешнего вида. Комментарии по шагам 
# объясняют различные настройки и установки для объектов кнопки.