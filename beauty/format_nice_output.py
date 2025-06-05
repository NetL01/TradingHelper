from datetime import datetime
from beauty.format_price import format_price

def format_nice_output(prices: dict, limits: dict) -> str:
    now = datetime.now().strftime("%H:%M")
    lines = []

    for symbol, price in prices.items():
        symbol_upper = symbol.upper()
        limit = limits.get(symbol.lower(), {})
        low = limit.get("low")
        high = limit.get("high")

        low_str = f"⬇️ {format_price(low)}" if low is not None else ""
        high_str = f"⬆️ {format_price(high)}" if high is not None else ""
        limit_parts = " | ".join(filter(None, [low_str, high_str]))
        limit_str = f"(limit: {limit_parts})" if limit_parts else ""

        line = f"  {symbol_upper:<10} ➤   ${format_price(price):<12} {limit_str}"
        lines.append(line)

    title = "📊   ТЕКУЩИЕ ЦЕНЫ\n"
    updated = f"\n\n🕒  ОБНОВЛЕНО: {now}"
    return title + "\n".join(lines) + updated
