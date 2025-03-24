import streamlit as st
import datetime
from collections import defaultdict

# Глобальные переменные для хранения данных
user_holidays = {}
schedules = {}

# Существующие праздники (можно расширить)
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
    st.subheader("Добавить свой праздник")
    date_input = st.date_input("Выберите дату праздника", min_value=datetime.date.today())
    holiday_name = st.text_input("Введите название праздника")
    if st.button("Добавить праздник"):
        if holiday_name.strip() == "":
            st.warning("Пожалуйста, введите название праздника.")
        else:
            formatted_date = date_input.strftime("%d-%m")
            user_holidays[formatted_date] = holiday_name
            st.success(f"Праздник '{holiday_name}' успешно добавлен!")

def view_calendar():
    """Просмотр календаря с праздниками"""
    st.subheader("Календарь праздников")
    selected_year = st.selectbox("Выберите год", range(datetime.date.today().year, datetime.date.today().year + 10))
    for month in range(1, 13):
        st.markdown(f"### Месяц: {datetime.date(1900, month, 1).strftime('%B')}")
        calendar_data = defaultdict(list)
        for day in range(1, 32):
            try:
                date = datetime.date(selected_year, month, day)
                formatted_date = date.strftime("%d-%m")
                if formatted_date in existing_holidays:
                    calendar_data[day].append(existing_holidays[formatted_date])
                if formatted_date in user_holidays:
                    calendar_data[day].append(user_holidays[formatted_date])
            except ValueError:
                continue
        if calendar_data:
            for day, holidays in calendar_data.items():
                st.write(f"{day} - {', '.join(holidays)}")
        else:
            st.write("Нет праздников в этом месяце.")

def create_schedule():
    """Создание расписания дня"""
    st.subheader("Создать расписание дня")
    date_input = st.date_input("Выберите дату", min_value=datetime.date.today())
    schedule_items = st.text_area("Введите расписание (одно событие на строку)")
    if st.button("Сохранить расписание"):
        if schedule_items.strip() == "":
            st.warning("Пожалуйста, введите расписание.")
        else:
            schedules[date_input] = [item.strip() for item in schedule_items.split("\n") if item.strip()]
            st.success(f"Расписание для {date_input.strftime('%d.%m.%Y')} успешно сохранено!")

def view_schedule():
    """Просмотр расписания дня"""
    st.subheader("Просмотр расписания")
    selected_date = st.date_input("Выберите дату для просмотра расписания", min_value=datetime.date.today())
    if selected_date in schedules:
        st.write(f"Расписание для {selected_date.strftime('%d.%m.%Y')}:")
        for idx, item in enumerate(schedules[selected_date], start=1):
            st.write(f"{idx}. {item}")
    else:
        st.info(f"Расписание для {selected_date.strftime('%d.%m.%Y')} не найдено.")

# Основной интерфейс приложения
st.title("Календарь праздников и расписаний")
menu = ["Добавить праздник", "Просмотр календаря", "Создать расписание", "Просмотр расписания"]

# Добавление выбора меню
choice = st.sidebar.selectbox("Меню", menu)

# Вызов соответствующей функции в зависимости от выбора пользователя
if choice == "Добавить праздник":
    add_user_holiday()
if choice == "Просмотр календаря":
    view_calendar()
if choice == "Создать расписание":
    create_schedule()
if choice == "Просмотр расписания":
    view_schedule()

# Отображение календаря после выбора меню
view_calendar()
