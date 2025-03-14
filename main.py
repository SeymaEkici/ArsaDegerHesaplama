import tkinter as tk
from tkinter import messagebox
from calculator import calculate_values
from currency import get_currency_rates
from design import setup_styles, create_label, create_entry, create_button

# Tkinter ana pencere
root = tk.Tk()
root.title("Arsa Değer Hesaplama")
root.geometry("650x850")  # Daha geniş ekran boyutu

setup_styles()  # Modern stilleri yükle

# Başlık etiketi
title_label = tk.Label(root, text="Arsa Değer Hesaplama", font=("Segoe UI", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=7, pady=10, sticky="n")

# **Sütun Başlıkları**
create_label(root, "Alım", 1, 1).config(font=("Segoe UI", 14, "bold"))
create_label(root, "Satış", 1, 3).config(font=("Segoe UI", 14, "bold"))

# **Fonksiyon: Tarih Otomatik Formatlama (DD.MM.YYYY)**
def format_date(entry_widget):
    text = entry_widget.get().replace(".", "").replace("/", "")
    if len(text) > 2:
        text = text[:2] + "." + text[2:]
    if len(text) > 5:
        text = text[:5] + "." + text[5:]
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, text)

# **Alım Bilgileri**
create_label(root, "Arsa Alım Tarihi:", 2, 1)
purchase_date_entry = create_entry(root, 2, 2)
purchase_date_entry.bind("<KeyRelease>", lambda event: format_date(purchase_date_entry))


create_label(root, "Metrekare(m²):", 3, 1)
square_meter_entry = create_entry(root, 3, 2)

create_label(root, "Arsa Alım Fiyatı (₺):", 4, 1)
purchase_price_entry = create_entry(root, 4, 2)


# **Satış Bilgileri**
create_label(root, "Arsa Satış Tarihi:", 2, 3)
sell_date_entry = create_entry(root, 2, 4)
sell_date_entry.bind("<KeyRelease>", lambda event: format_date(sell_date_entry))

create_label(root, "Metrekare(m²):", 3, 3)
sell_square_meter_entry = create_entry(root, 3, 4)

create_label(root, "Arsa Satış Fiyatı(₺):", 4, 3)
sell_price_entry = create_entry(root, 4, 4)


# **Sonuç Kutusu**
results_frame = tk.Frame(root, bg="#F4F4F4", padx=15, pady=15)
results_frame.grid(row=6, column=1, columnspan=4, pady=10, sticky="nsew")
results_frame.grid_remove()

# **Alım - Satış Sonuçları Başlıkları**
create_label(results_frame, "Alım Karşılığı", 0, 1).config(font=("Segoe UI", 12, "bold"))
create_label(results_frame, "Satış Karşılığı", 0, 2).config(font=("Segoe UI", 12, "bold"))

# **Alım Sonuçları**
purchase_usd_label = create_label(results_frame, "-", 1, 1)
purchase_eur_label = create_label(results_frame, "-", 2, 1)
purchase_gold_label = create_label(results_frame, "-", 3, 1)
purchase_m2_label = create_label(results_frame, "m² Başına Fiyat: - ₺", 4, 1)  # **m² fiyatı düzgün konumlandırıldı**

# **Satış Sonuçları**
sell_usd_label = create_label(results_frame, "-", 1, 2)
sell_eur_label = create_label(results_frame, "-", 2, 2)
sell_gold_label = create_label(results_frame, "-", 3, 2)
sell_m2_label = create_label(results_frame, "m² Başına Fiyat: - ₺", 4, 2)  # **m² fiyatı düzgün konumlandırıldı**

# **Boşluk Ekleyerek Daha Net Bir Ayrım**
create_label(results_frame, "", 5, 1)
create_label(results_frame, "", 5, 2)

# **Değişim Sonuçları Başlığı (Belirgin Hale Getirildi)**
change_label = tk.Label(results_frame, text="--- Değişim Sonuçları ---", font=("Segoe UI", 12, "bold"))
change_label.grid(row=6, column=1, columnspan=2, pady=10, sticky="n")

# **Ortalanmış Değişim Sonuçları**
change_frame = tk.Frame(results_frame, bg="#F4F4F4")
change_frame.grid(row=7, column=1, columnspan=2, pady=5)

usd_result_label = create_label(change_frame, "-", 1, 1)
eur_result_label = create_label(change_frame, "-", 2, 1)
gold_result_label = create_label(change_frame, "-", 3, 1)
m2_result_label = create_label(change_frame, "-", 4, 1)
total_price_change_label = create_label(change_frame, "-", 5, 1)
m2_price_change_label = create_label(change_frame, "-", 6, 1)

# **Hesaplama Butonu**
calculate_button = create_button(root, "HESAPLA", lambda: on_calculate(), 5, 2)
calculate_button.grid(row=5, column=2, columnspan=2, pady=15)

# **Hesaplama Fonksiyonu**
def format_number(value, is_percentage=False):
    """1000'lik basamaklara ayırır, yüzdelik değerlerde uygulanmaz"""
    return f"{value:,.2f}".replace(",", ".") if not is_percentage else f"{value:.2f}"

def on_calculate():
    try:
        purchase_date = purchase_date_entry.get()
        sell_date = sell_date_entry.get()
        square_meter = float(square_meter_entry.get())
        purchase_price = float(purchase_price_entry.get())
        sell_price = float(sell_price_entry.get())

        result = calculate_values(purchase_date, sell_date, square_meter, purchase_price, sell_price)

        if "error" in result:
            messagebox.showerror("Hata", result["error"])
            return

        purchase_rates = get_currency_rates(purchase_date)
        sell_rates = get_currency_rates(sell_date)

        if not purchase_rates or not sell_rates:
            messagebox.showerror("Hata", "Döviz veya altın kuru alınamadı. Lütfen tarihleri kontrol edin!")
            return

        # **Alım Karşılığı - Hesaplanan Kur Değerleri Eklenmiş Hali**
        purchase_usd_label.config(text=f"Dolar Karşılığı: {format_number(result['purchase_price_usd'])} $ (Kur: {format_number(purchase_rates['USD'])} ₺)")
        purchase_eur_label.config(text=f"Euro Karşılığı: {format_number(result['purchase_price_eur'])} € (Kur: {format_number(purchase_rates['EUR'])} ₺)")
        purchase_gold_label.config(text=f"Altın Karşılığı: {format_number(result['purchase_price_gold'])} gr (Kur: {format_number(purchase_rates['GOLD'])} ₺)")
        purchase_m2_label.config(text=f"m² Başına Fiyat: {format_number(result['purchase_m2_tl'])} ₺")

        # **Satış Karşılığı - Hesaplanan Kur Değerleri Eklenmiş Hali**
        sell_usd_label.config(text=f"Dolar Karşılığı: {format_number(result['sell_price_usd'])} $ (Kur: {format_number(sell_rates['USD'])} ₺)")
        sell_eur_label.config(text=f"Euro Karşılığı: {format_number(result['sell_price_eur'])} € (Kur: {format_number(sell_rates['EUR'])} ₺)")
        sell_gold_label.config(text=f"Altın Karşılığı: {format_number(result['sell_price_gold'])} gr (Kur: {format_number(sell_rates['GOLD'])} ₺)")
        sell_m2_label.config(text=f"m² Başına Fiyat: {format_number(result['sell_m2_tl'])} ₺")

        # **DEĞİŞİM KISMINI EKLEYELİM (GÖZÜKMÜYORDU)**
        usd_result_label.config(text=f"Dolar Değişim: {format_number(result['change_usd'], True)}%")
        eur_result_label.config(text=f"Euro Değişim: {format_number(result['change_eur'], True)}%")
        gold_result_label.config(text=f"Altın Değişim: {format_number(result['change_gold'], True)}%")
        m2_result_label.config(text=f"Fiyat Değişim (m²): {format_number(result['change_m2'], True)}%")
        total_price_change_label.config(text=f"Toplam Fiyat Değişimi: {format_number(result['change_tl'], True)}%")
        


        results_frame.grid()

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli sayılar giriniz!")

# Pencere çalıştırılıyor
root.mainloop()
