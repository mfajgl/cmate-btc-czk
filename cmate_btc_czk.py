import json
import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # ✅ pro český čas

URL = "https://coinmate.io/api/ticker?currencyPair=BTC_CZK"
DATA_FILE = "cmate_btc_data.json"
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
    """Načte existující JSON data (bez pádu, i když je prázdný)."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print("⚠️ Poškozený JSON – vytvářím nový soubor.")
            return []
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

    local_time = datetime.now(ZoneInfo("Europe/Prague")).strftime("%Y-%m-%d %H:%M:%S")

    data = load_data()
    new_entry = {"time": local_time, "price_czk": price}
    data.append(new_entry)

    if len(data) > MAX_ENTRIES:
        data = data[-MAX_ENTRIES:]

    save_data(data)

    print(f"✅ Uloženo {len(data)} záznamů. Poslední cena: {price} CZK ({local_time})")


if __name__ == "__main__":
    main()
