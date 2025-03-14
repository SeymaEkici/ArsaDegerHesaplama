from currency import get_currency_rates


def calculate_values(purchase_date, sell_date, square_meter, purchase_price, sell_price):
    try:
        purchase_rates = get_currency_rates(purchase_date)
        sell_rates = get_currency_rates(sell_date)

        if not purchase_rates or not sell_rates:
            return {"error": "Döviz veya altın kuru alınamadı!"}

        # Satın alma ve satış fiyatlarını aynen kullan
        purchase_price_usd = purchase_price / purchase_rates["USD"]
        purchase_price_eur = purchase_price / purchase_rates["EUR"]
        purchase_price_gold = purchase_price / purchase_rates["GOLD"]

        sell_price_usd = sell_price / sell_rates["USD"]
        sell_price_eur = sell_price / sell_rates["EUR"]
        sell_price_gold = sell_price / sell_rates["GOLD"]

        # Değişim hesaplamaları (yüzde olarak)
        change_usd = ((sell_price_usd - purchase_price_usd) / purchase_price_usd) * 100
        change_eur = ((sell_price_eur - purchase_price_eur) / purchase_price_eur) * 100
        change_gold = ((sell_price_gold - purchase_price_gold) / purchase_price_gold) * 100
        change_m2 = ((sell_price / square_meter - purchase_price / square_meter) / (purchase_price / square_meter)) * 100
        change_tl = ((sell_price - purchase_price) / purchase_price) * 100
        change_m2_price = ((sell_price / square_meter) - (purchase_price / square_meter)) / (purchase_price / square_meter) * 100

        # Metrekare başına fiyatlar
        purchase_m2_tl = purchase_price / square_meter
        sell_m2_tl = sell_price / square_meter

        return {
            "purchase_price_usd": purchase_price_usd,
            "purchase_price_eur": purchase_price_eur,
            "purchase_price_gold": purchase_price_gold,
            "sell_price_usd": sell_price_usd,
            "sell_price_eur": sell_price_eur,
            "sell_price_gold": sell_price_gold,
            "change_usd": change_usd,
            "change_eur": change_eur,
            "change_gold": change_gold,
            "change_m2": change_m2,
            "change_tl": change_tl,
            "change_m2_price": change_m2_price,
            "purchase_m2_tl": purchase_m2_tl,
            "sell_m2_tl": sell_m2_tl,
        }

    except Exception as e:
        return {"error": str(e)}
