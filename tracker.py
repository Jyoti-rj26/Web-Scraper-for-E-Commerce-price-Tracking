# tracker.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from config import URL, HEADERS, SELECTORS

def get_product_info():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        title = soup.find(SELECTORS["title"]["tag"], class_=SELECTORS["title"]["class"]).get_text(strip=True)
        price = soup.find(SELECTORS["price"]["tag"], class_=SELECTORS["price"]["class"]).get_text(strip=True)
    except AttributeError:
        title = "N/A"
        price = "N/A"

    return title, price

def save_price_data(name, price):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([{
        "Time": pd.Timestamp.now(),
        "Product": name,
        "Price": price
    }])
    file_path = "data/prices.csv"
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

def main():
    print("Starting price tracker...")
    while True:
        name, price = get_product_info()
        save_price_data(name, price)
        print(f"[{pd.Timestamp.now()}] {name} - {price}")
        time.sleep(3600)  # Run every hour

if __name__ == "__main__":
    main()
