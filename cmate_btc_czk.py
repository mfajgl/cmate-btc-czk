import json
import requests
from datetime import datetime


API_URL = "https://coinmate.io/api/ticker?currencyPair=BTC_CZK"
JSON_FILE = "cmate_btc_data.json"
MAX_ENTRIES = 45


def get_btc_price():
response = requests.get(API_URL)
data = response.json()
return float(data["data"]["last"])


def load_data():
try:
with open(JSON_FILE, "r") as f:
return json.load(f)
except FileNotFoundError:
return []


def save_data(data):
with open(JSON_FILE, "w") as f:
json.dump(data, f, indent=2, ensure_ascii=False)


def main():
btc_price = get_btc_price()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


data = load_data()
data.append({"datetime": timestamp, "btc_czk": btc_price})


if len(data) > MAX_ENTRIES:
data = data[-MAX_ENTRIES:]


save_data(data)
print(f"✅ Uložena cena {btc_price:.2f} CZK v {timestamp}")


if __name__ == "__main__":
main()
