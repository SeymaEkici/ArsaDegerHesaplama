import tkinter as tk
from tkinter import ttk

def setup_styles():
    """Tkinter bileşenleri için modern stiller belirler"""
    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 11), padding=10, background="#0078D7", foreground="black")
    style.configure("TLabel", font=("Segoe UI", 11), background="#F4F4F4")
    style.configure("TEntry", font=("Segoe UI", 11), padding=5)

def create_label(root, text, row, column):
    """Standart bir etiket oluşturur"""
    label = ttk.Label(root, text=text)
    label.grid(row=row, column=column, padx=10, pady=5, sticky="w")
    return label

def create_entry(root, row, column):
    """Standart bir giriş alanı (entry) oluşturur"""
    entry = ttk.Entry(root)
    entry.grid(row=row, column=column, padx=10, pady=5)
    return entry

def create_button(root, text, command, row, column):
    """Modern bir buton oluşturur"""
    button = ttk.Button(root, text=text, command=command, style="TButton")
    button.grid(row=row, column=column, pady=20)
    return button
