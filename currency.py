import pandas as pd
from datetime import datetime

# Excel dosya yolu (Bilgisayarında doğru konumu yaz)
file_path = r"C:\Users\sydme\Desktop\noo.xlsx"

# Excel dosyasını aç
xls = pd.ExcelFile(file_path)

# Sayfa adlarını kontrol et ve doğru olanı seç
print("Excel'deki Sayfa İsimleri:", xls.sheet_names)
sheet_name = "Geçmiş Kur" if "Geçmiş Kur" in xls.sheet_names else xls.sheet_names[0]

# Excel'deki döviz kurlarını oku
df_gecmis_kur = pd.read_excel(xls, sheet_name=sheet_name)

# Gerekli sütunları al ve isimlendir
df_gecmis_kur = df_gecmis_kur[['Tarih', 'TP DK USD A YTL', 'TP DK EUR A YTL', 'altın gram']]
df_gecmis_kur.columns = ['Tarih', 'USD', 'EUR', 'GOLD']

# Tarih sütununu datetime formatına çevir
df_gecmis_kur['Tarih'] = pd.to_datetime(df_gecmis_kur['Tarih'], errors='coerce')

# USD, EUR ve GOLD sütunlarını float formatında bırak (Yuvarlama yapmayacak)
df_gecmis_kur[['USD', 'EUR', 'GOLD']] = df_gecmis_kur[['USD', 'EUR', 'GOLD']].apply(pd.to_numeric, errors='coerce')


def get_currency_rates(date):
    """
    Verilen tarihe en yakın döviz ve altın kurlarını döndürür.
    Excel'deki tam değerleri aynen kullanır.
    """
    try:
        date = pd.to_datetime(date)  # Tarihi datetime formatına çevir
        df_filtered = df_gecmis_kur[df_gecmis_kur['Tarih'] <= date].sort_values(by='Tarih', ascending=False)

        if not df_filtered.empty:
            rates = df_filtered.iloc[0][['USD', 'EUR', 'GOLD']].to_dict()

            # Eğer altın kuru NaN ise, en yakın bulunan değeri al
            if pd.isna(rates["GOLD"]):
                df_gold_filled = df_gecmis_kur[df_gecmis_kur['GOLD'].notna()].sort_values(by='Tarih', ascending=False)
                closest_gold = df_gold_filled.iloc[0]["GOLD"] if not df_gold_filled.empty else None
                rates["GOLD"] = closest_gold

            # Döviz kurlarını olduğu gibi döndür (Yuvarlamadan)
            return rates
        else:
            return None
    except Exception as e:
        print(f"Döviz kuru okunurken hata oluştu: {e}")
        return None
