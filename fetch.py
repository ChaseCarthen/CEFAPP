import requests
from typing import List

import json

CEFS = ['GUT', 'UTF', 'PDI', 'GOF', 'DNP', 'ETG', 'EVT', 'EXG', 'HTD']
BASE_PRICE_URL = "https://www.cefconnect.com/api/v3/pricinghistory/{}/1Y"
BASE_DIV_URL = "https://www.cefconnect.com/api/v3/distributionhistory/fund/{}/{}/{}"
# https://www.cefconnect.com/api/v3/distributionhistory/fund/${selectedTicker}/${distStartDate}/${distEndDate}`

# https://www.cefconnect.com/api/v3/pricinghistory/${selectedTicker}/1Y
def fetch_cef_price_nav(ticker: str):
    try:
        url = BASE_PRICE_URL.format(ticker)
        response = requests.get(url,headers={ "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0" })
        response.raise_for_status()
        data = response.json()
        price_history = data.get("Data", {}).get("PriceHistory", [])
        if not price_history:
            print(f"[{ticker}] No price history available.")
            return None

        latest = price_history[-1]
        price = float(latest.get("Data", 0))
        nav = float(latest.get("NAVData", 0))
        return price, nav
    except Exception as e:
        print(f"[{ticker}] Error fetching data: {e}")
        return None

def fetch_historic_cef_price_nav(ticker: str):
    try:
        url = BASE_PRICE_URL.format(ticker)
        response = requests.get(url, headers={ "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0" })
        response.raise_for_status()
        data = response.json()
        price_history = data.get("Data", {}).get("PriceHistory", [])
        if not price_history:
            print(f"[{ticker}] No price history available.")
            return None

        prices = [(entry.get("DataDate"), float(entry.get("Data", 0)), float(entry.get("NAVData", 0))) for entry in price_history]
        return prices
    except Exception as e:
        print(f"[{ticker}] Error fetching historic data: {e}")
        return None

def fetch_cef_dividends(ticker: str, start_date: str, end_date: str):
    try:
        url = BASE_DIV_URL.format(ticker, start_date, end_date)
        response = requests.get(url, headers={ "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0" })
        response.raise_for_status()
        data = response.json()
        return data.get("Data", [])
    except Exception as e:
        print(f"[{ticker}] Error fetching dividends: {e}")
        return []


def evaluate_cefs(cefs: List[str]):
    recommendations = []
    for ticker in cefs:
        result = fetch_cef_price_nav(ticker)
        if result:
            price, nav = result
            action = "BUY" if price < nav else "DO NOT BUY"
            print(f"{ticker}: Price=${price:.2f}, NAV=${nav:.2f} → {action}")
            recommendations.append((ticker, price, nav, action))
    return recommendations

if __name__ == "__main__":
    print("Evaluating CEFs based on Selengut's NAV strategy...\n")
    evaluate_cefs(CEFS)

