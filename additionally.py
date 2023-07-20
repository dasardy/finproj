from datetime import datetime

def convert_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d.%m")
    return formatted_date

gradColor = ["#F23B67", "#352958"]
textColor = "#352958"
allfonts= {
    'PantonBold' :"https://raw.githubusercontent.com/dasardy/popop/main/Panton-SemiBold%20(2).ttf",
    'Panton': "https://raw.githubusercontent.com/dasardy/popop/master/PANTON-REGULAR%20(3).OTF",
    }
    
def convert_date_calendar(date_tuple1, date_tuple2):
    month1, day1, year1 = date_tuple1
    month2, day2, year2 = date_tuple2
    date1 = f"{year1}-{month1}-{day1}"
    date2 = f"{year2}-{month2}-{day2}"
    new_date1 = datetime.strptime(date1, "%Y-%m-%d")
    new_date2 = datetime.strptime(date2, "%Y-%m-%d")
    date_list = []
    if new_date1 > new_date2:
        date_list.append(new_date2.strftime("%Y-%m-%d"))
        date_list.append(new_date1.strftime("%Y-%m-%d"))
    else:
        date_list.append(new_date1.strftime("%Y-%m-%d"))
        date_list.append(new_date2.strftime("%Y-%m-%d"))
    return date_list



# Функция convert_date(date) преобразует дату из формата YYYY-MM-DD в формат DD.MM.

# Функция convert_date_calendar(date_tuple1, date_tuple2) преобразует даты из кортежей 
# в формате (месяц, день, год) в список двух элементов, где первый элемент является 
# более ранней датой, а второй элемент - более поздней датой в формате YYYY-MM-DD.

# Переменные gradColor, textColor и allfonts содержат некоторые цвета и ссылки на шрифты, используемые в проекте.