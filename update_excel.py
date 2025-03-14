import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 1) Doviz.com'dan USD, EUR ve ALTIN gram alış değerlerini çekme fonksiyonu
def get_new_exchange_data():
    """
    Bu fonksiyon doviz.com ana sayfasına istek atar,
    gelen HTML içinden USD, EUR ve ALTIN gram fiyatını bulur
    ve (tarih, usd, eur, gold) şeklinde döndürür.
    """
    url = "https://www.tcmb.gov.tr/kurlar/today.xml"  # doviz.com ana sayfa
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # NOT: Aşağıdaki seçimler (soup.select_one) sitedeki HTML'ye göre ayarlanmıştır.
    # Site yapısı değişirse bu kısımları güncellemeniz gerekir.
    usd_element = soup.select_one("span.menu-row2-item.js-data-usd")
    eur_element = soup.select_one("span.menu-row2-item.js-data-eur")
    gold_element = soup.select_one("span.menu-row2-item.js-data-gram-altin")

    # Bulunan metin değerlerini float sayıya çevirelim (örn: "19,00" -> 19.00)
    def parse_price(text):
        return float(text.replace(",", ".").strip())

    usd = parse_price(usd_element.text) if usd_element else None
    eur = parse_price(eur_element.text) if eur_element else None
    gold = parse_price(gold_element.text) if gold_element else None

    # Tarih olarak bugünü al
    today_str = datetime.now().strftime("%Y-%m-%d")

    return (today_str, usd, eur, gold)


# 2) Excel dosyamızı güncelleyen fonksiyon
def update_excel_with_new_rates():
    """
    1) get_new_exchange_data() ile yeni kurları alır
    2) C:\Users\sydme\Desktop\gecmis_kur.xlsx dosyasını okur
    3) Yeni satırı ekleyip kaydeder
    """
    # Dosya yolunu raw string veya çift ters slash şeklinde yazın
    excel_path = r"C:\Users\sydme\Desktop\kur.xlsx"

    # 2.1) Yeni kurları al
    tarih, usd, eur, gold = get_new_exchange_data()

    print("Bugünkü kurlar:")
    print("Tarih:", tarih, "USD:", usd, "EUR:", eur, "Altın:", gold)

    # 2.2) Excel'i oku
    df_existing = pd.read_excel(excel_path, sheet_name="Geçmiş Kur")

    # 2.3) Yeni satır hazırlama
    new_row = {
        "Tarih": tarih,
        "USD": usd,
        "EUR": eur,
        "GOLD": gold
    }

    # 2.4) DataFrame'e ekleme (append yerine concat kullanıyoruz)
    df_new = pd.DataFrame([new_row])
    df_updated = pd.concat([df_existing, df_new], ignore_index=True)

    # 2.5) Geri yaz
    df_updated.to_excel(excel_path, sheet_name="Geçmiş Kur", index=False)
    print("Excel dosyası güncellendi:", excel_path)


# Dosya doğrudan çalıştırıldığında güncelleme fonksiyonunu çağır
if __name__ == "__main__":
    update_excel_with_new_rates()
