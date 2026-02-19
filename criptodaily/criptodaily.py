import requests
from statistics import mean
from rich.console import Console
from rich.text import Text

# =====================
# Configuração
# =====================

COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
#    "pepe": "PEPE",
}

VS_CURRENCY = "usd"
DAYS_HISTORY = 30
MA_PERIODS = 10
API_BASE = "https://api.coingecko.com/api/v3"

console = Console()

# =====================
# Utilidades
# =====================

def format_price(symbol, price):
    if price is None:
        return "—"
    return f"${price:,.6f}" if symbol == "PEPE" else f"${price:,.0f}"


def variation_text(pct):
    if pct is None:
        return Text("—", style="yellow")
    arrow = "▲" if pct >= 0 else "▼"
    color = "green" if pct >= 0 else "red"
    return Text(f"{arrow} {pct:.2f}%", style=color)


def trend_arrow(prices):
    if len(prices) < MA_PERIODS:
        return Text("→", style="yellow")
    ma = mean(prices[-MA_PERIODS:])
    return Text("↑", "green") if prices[-1] > ma else Text("↓", "red")


def volume_label(volume_24h, volumes_30d):
    if not volumes_30d:
        return Text("—", style="yellow")

    avg = mean(volumes_30d)
    if volume_24h > avg * 1.15:
        return Text(f"Alto {volume_24h/1e9:.1f}M", style="green")
    if volume_24h < avg * 0.85:
        return Text(f"Baixo {volume_24h/1e9:.1f}M", style="red")
    return Text(f"Médio {volume_24h/1e9:.1f}M", style="yellow")

# =====================
# API
# =====================

def get_market_data():
    url = f"{API_BASE}/coins/markets"
    params = {
        "vs_currency": VS_CURRENCY,
        "ids": ",".join(COINS),
        "price_change_percentage": "24h",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else []
    except requests.RequestException:
        return []


def get_history(coin_id):
    url = f"{API_BASE}/coins/{coin_id}/market_chart"
    params = {"vs_currency": VS_CURRENCY, "days": DAYS_HISTORY}
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else {}
    except requests.RequestException:
        return {}

# =====================
# Interface ASCII
# =====================

def print_header():
    console.print("\n[cyan]Crypto Daily - Buying high & Selling low[/cyan] ")
    console.print("─" * 90)
    console.print(
        "| Ticker | Preço      | Var 24h | Máx 30d   | Mín 30d   | Volume 24h    | Trend |"
    )
    console.print("=" * 90)


def print_row(ticker, price, variation, max_30d, min_30d, volume, trend):
    console.print(
        f"| {ticker:<6} | "
        f"{price:>10} | ",
        variation,
        f" | {max_30d:>9} | {min_30d:>9} | ",
        volume,
        f" | ",
        trend,
        " |",
        sep=""
    )


def print_monitor():
    print_header()

    data = get_market_data()
    if not data:
        console.print("[red]Sem dados (rate limit ou erro de rede)[/red]")
        return

    for coin in data:
        cid = coin["id"]
        symbol = COINS[cid]

        history = get_history(cid)
        prices = [p[1] for p in history.get("prices", [])]
        volumes = [v[1] for v in history.get("total_volumes", [])]

        print_row(
            ticker=symbol,
            price=format_price(symbol, coin.get("current_price")),
            variation=variation_text(coin.get("price_change_percentage_24h")),
            max_30d=format_price(symbol, max(prices)) if prices else "—",
            min_30d=format_price(symbol, min(prices)) if prices else "—",
            volume=volume_label(coin.get("total_volume", 0), volumes),
            trend=trend_arrow(prices),
        )
        
# =====================
# Execução
# =====================

if __name__ == "__main__":
    print_monitor()
    console.print()
