import tkinter as tk

# Tkinter giriş alanı oluşturma fonksiyonu
def create_label_entry(root, label_text, row, column):
    label = tk.Label(root, text=label_text)
    label.grid(row=row, column=column)
    entry = tk.Entry(root)
    entry.grid(row=row, column=column + 1)
    return entry

# Tkinter sonuç etiketi oluşturma fonksiyonu
def create_result_label(root, text, row, column):
    label = tk.Label(root, text=text)
    label.grid(row=row, column=column)
    return label
