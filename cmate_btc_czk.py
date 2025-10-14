import json
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # ✅ pro český čas

# URL Coinmate API pro cenu BTC/CZK
URL = "https://coinmate.io/api/ticker?currencyPair=BTC_CZK"

# Název JSON souboru, kam se ukládají data
DATA_FILE = "cmate_btc_data.json"

# Maximální počet záznamů v souboru
MAX_ENTRIES = 45


def fetch_btc_price():
    """Získá aktuální cenu BTC v CZK z Coinmate API."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data_json = response.json()
        return data_json.get("data", {}).get("last", None)
    except Exception as e:
        print(f"❌ Chyba při získávání dat: {e}")
        return None


def load_data():
    """Načte existující JSON data (nebo vytvoří nový seznam)."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    """Uloží data zpět do JSON souboru."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    price = fetch_btc_price()
    if price is None:
        print("⚠️ Cena BTC nebyla získána.")
        return

    # ✅ aktuální čas v české zóně (automaticky CEST/CET)
    local_time = datetime.now(ZoneInfo("Europe/Prague")).strftime("%Y-%m-%d %H:%M:%S")

    # načti existující data
    data = load_data()

    # přidej nový záznam
    new_entry = {
        "time": local_time,
        "price_czk": price
    }
    data.append(new_entry)

    # omez na posledních 45 záznamů
    if len(data) > MAX_ENTRIES:
        data = data[-MAX_ENTRIES:]

    # ulož zpět
    save_data(data)

    print(f"✅ Uloženo {len(data)} záznamů. Poslední cena: {price} CZK ({local_time})")


if __name__ == "__main__":
    main()
