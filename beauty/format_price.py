def format_price(price: float) -> str:
    if price >= 1:
        return f"{price:,.2f}"
    else:
        return f"{price:.6f}".rstrip('0').rstrip('.')