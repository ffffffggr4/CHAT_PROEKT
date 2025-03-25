import datetime
from collections import defaultdict
import json
import os

# Глобальные переменные для хранения данных
user_holidays = {}
schedules = {}

# Загрузка данных из файла (если есть)
def load_data():
    global user_holidays, schedules
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            user_holidays = data.get("user_holidays", {})
            schedules = data.get("schedules", {})
    except FileNotFoundError:
        pass

# Сохранение данных в файл
def save_data():
    with open("data.json", "w") as file:
        json.dump({"user_holidays": user_holidays, "schedules": schedules}, file)

# Существующие праздники
existing_holidays = {
    "01-01": "Новый год 🎉",
    "23-02": "День защитника Отечества ⚔️",
    "08-03": "Международный женский день 🌸",
    "01-05": "Праздник весны и труда 🍃",
    "09-05": "День Победы 🌟",
    "12-06": "День России 🇷🇺",
    "04-11": "День народного единства 🕊️"
}

def add_user_holiday():
    """Добавление пользовательского праздника"""
    print("\n--- Добавить свой праздник ---")
    while True:
        try:
            date_input = input("Введите дату праздника (формат: DD-MM-YYYY): ")
            date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
            if date < datetime.date.today():
                print("Ошибка: Дата должна быть сегодня или позже.")
                continue
            break
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте формат DD-MM-YYYY.")
    
    holiday_name = input("Введите название праздника: ").strip()
    if holiday_name == "":
        print("Ошибка: Название праздника не может быть пустым.")
        return
    
    formatted_date = date.strftime("%d-%m")
    user_holidays[formatted_date] = holiday_name
    save_data()
    print(f"Праздник '{holiday_name}' успешно добавлен!")

def view_calendar():
    """Просмотр календаря с праздниками"""
    print("\n--- Календарь праздников ---")
    year = int(input("Введите год для просмотра календаря: "))
    for month in range(1, 13):
        print(f"\nМесяц: {datetime.date(1900, month, 1).strftime('%B')}")
        calendar_data = defaultdict(list)
        for day in range(1, 32):
            try:
                date = datetime.date(year, month, day)
                formatted_date = date.strftime("%d-%m")
                if formatted_date in existing_holidays:
                    calendar_data[day].append(existing_holidays[formatted_date])
                if formatted_date in user_holidays:
                    calendar_data[day].append(user_holidays[formatted_date])
            except ValueError:
                continue
        if calendar_data:
            for day, holidays in calendar_data.items():
                print(f"{day} - {', '.join(holidays)}")
        else:
            print("Нет праздников в этом месяце.")

def create_schedule():
    """Создание расписания дня"""
    print("\n--- Создать расписание дня ---")
    while True:
        try:
            date_input = input("Введите дату для создания расписания (формат: DD-MM-YYYY): ")
            date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
            if date < datetime.date.today():
                print("Ошибка: Дата должна быть сегодня или позже.")
                continue
            break
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте формат DD-MM-YYYY.")
    
    schedule_items = input("Введите расписание (одно событие на строку, завершите ввод пустой строкой):\n")
    items = []
    while schedule_items.strip() != "":
        items.append(schedule_items.strip())
        schedule_items = input()
    
    if not items:
        print("Ошибка: Расписание не может быть пустым.")
        return
    
    schedules[str(date)] = items
    save_data()
    print(f"Расписание для {date.strftime('%d.%m.%Y')} успешно сохранено!")

def view_schedule():
    """Просмотр расписания дня"""
    print("\n--- Просмотр расписания ---")
    while True:
        try:
            date_input = input("Введите дату для просмотра расписания (формат: DD-MM-YYYY): ")
            date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
            break
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте формат DD-MM-YYYY.")
    
    date_str = str(date)
    if date_str in schedules:
        print(f"Расписание для {date.strftime('%d.%m.%Y')}:")
        for idx, item in enumerate(schedules[date_str], start=1):
            print(f"{idx}. {item}")
    else:
        print(f"Расписание для {date.strftime('%d.%m.%Y')} не найдено.")

def main_menu():
    """Главное меню приложения"""
    while True:
        print("\n--- Главное меню ---")
        print("1. Добавить праздник")
        print("2. Просмотр календаря")
        print("3. Создать расписание")
        print("4. Просмотр расписания")
        print("5. Выход")
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == "1":
            add_user_holiday()
        elif choice == "2":
            view_calendar()
        elif choice == "3":
            create_schedule()
        elif choice == "4":
            view_schedule()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: Неверный выбор. Пожалуйста, выберите от 1 до 5.")

if __name__ == "__main__":
    # Загрузка данных
    load_data()
    # Запуск главного меню
    main_menu()
