# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import json
from contextlib import closing
import requests
import sqlite3
import plotly.express as px

STICKER_CAPSULE_1 = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=2&market_hash_name=Community%20Sticker%20Capsule%201"
DATABASE_NAME = "price_database.db"

def main():
    r = requests.get(STICKER_CAPSULE_1)
    print(r.text)

    items = getFromDatabase("SELECT * FROM item_paths")

    prices = []
    for item in items:
        prices.append((makePriceRequest(item[2]), datetime.datetime.now(), item[0]))

    insertIntoDatabase("INSERT INTO price_history(price, date, item_id) VALUES(?,?,?)", prices)
    prices = getFromDatabase("SELECT * FROM price_history")

    priceData = {}
    for price in prices:



def makePriceRequest(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return json.loads(response.text)["lowest_price"]

def getFromDatabase(sql):
    with closing(getConnection()) as conn:
        with closing(conn.cursor()) as cursor:
            rows = cursor.execute(
                sql
            )

    return rows

def insertIntoDatabase(sql, values):
    with closing(getConnection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executemany(sql, values)

def getConnection():
    return sqlite3.connect(DATABASE_NAME)

def createTables():
    with closing(getConnection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS item_paths(id INTEGER PRIMARY KEY, item_name TEXT NOT NULL, item_path TEXT NOT NULL)')
            cursor.execute('CREATE TABLE IF NOT EXISTS price_history(id INTEGER PRIMARY KEY, price INTEGER NOT NULL, date TEXT NOT NULL, item_id INTEGER NOT NULL, FOREIGN KEY(item_id) REFERENCES item_paths(id)')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
