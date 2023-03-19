import os
import requests
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import creds
import psycopg2
from psycopg2 import sql
import schedule
import time
from googleapiclient.discovery import build


def get_service_simple():
    """
    Функция создает объект сервиса Google Sheets API с использованием API-ключа.
    :return: объект сервиса Google Sheets API
    """
    return build('sheets', 'v4', developerKey=creds.api_key)


def get_service_sacc():
    """
    Функция создает объект сервиса Google Sheets API с использованием сервисного аккаунта.
    Может читать и (возможно) писать в таблицы, к которым выдан доступ.
    :return: объект сервиса Google Sheets API
    """
    creds_json = os.path.dirname(__file__) + "\creds\disco-stock-380706-b5c4040d3a48.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


# Используем функцию get_service_sacc() для получения объекта сервиса Google Sheets API с использованием сервисного аккаунта
service = get_service_sacc()
sheet = service.spreadsheets()

# ID таблицы Google Sheets, которую мы будем читать
sheet_id = "1hAe1Gch-vJkpjE3Y7Q-XxAii_WzwNS9N3tb96qv4z3U"

# Читаем данные из таблицы Google Sheets
# В данном примере мы читаем данные из диапазона ячеек A2:D на листе Лист1

resp = sheet.values().get(spreadsheetId=sheet_id, range="Лист1!A2:D").execute()

# Выводим полученные данные

print(resp)



def get_database_connection():
    """
       Получение подключения к базе данных
    """
    conn = psycopg2.connect(
        port="5432",
        dbname="НАЗВАНИЕ БД",
        user="ИМЯ ПОЛЬЗОВАТЕЛЯ",
        password="ПАРОЛЬ"
    )
    return conn




def get_exchange_rate(currency):
    """
    Получение текущего курса обмена для указанной валюты
    """
    response = requests.get(f"https://www.cbr-xml-daily.ru/daily_json.js")
    response_json = response.json()
    exchange_rate = response_json["Valute"][currency]["Value"]
    return exchange_rate

def convert_currency(amount, exchange_rate):
    """
    Конвертирование валюты по заданному курсу
    """
    return amount * exchange_rate


def insert_data_to_postgresql(data):
    """
       Вставка данных в таблицу базы данных
    """
    conn = get_database_connection()
    with conn.cursor() as cur:
        cur.execute(sql.SQL("DELETE FROM my_table"))

        # Получение курса обмена для доллара США
        exchange_rate = get_exchange_rate("USD")
        for row in data:
            cur.execute(
                sql.SQL("INSERT INTO my_table (name, order_number, price, date) VALUES ({}, {}, {}, {})").format(
                    sql.Literal(row[0]), sql.Literal(row[1]), sql.Literal(row[2]),
                    sql.SQL("TO_DATE({}, 'DD.MM.YYYY')").format(sql.Literal(row[3]))
                )
            )
            # Расчет цены в рублях и вставка ее в базу данных
            price_usd = float(row[2])
            price_rub = convert_currency(price_usd, exchange_rate)
            cur.execute(
                sql.SQL("UPDATE my_table SET price_rub = {} WHERE order_number = {}").format(
                    sql.Literal(price_rub), sql.Literal(row[1])
                )
            )
        conn.commit()

# Получение данных из Google Sheets
resp = sheet.values().get(spreadsheetId=sheet_id, range="Лист1!A2:D").execute()
data = resp.get("values", [])

# Вставка данных в базу данных
insert_data_to_postgresql(data)

def update_data():
    """
        Обновление данных в базе данных
    """
    resp = sheet.values().get(spreadsheetId=sheet_id, range="Лист1!A2:D").execute()
    data = resp.get("values", [])
    insert_data_to_postgresql(data)

# Установка расписания обновления данных
schedule.every(1).minutes.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(1)

