import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
import os
import sys
import pandas as pd

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_database():
    db_path = resource_path('workers.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS workers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    worker_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    meal_amount REAL NOT NULL,
                    FOREIGN KEY(worker_id) REFERENCES workers(id)
                )''')
    conn.commit()
    conn.close()

create_database()

class WorkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YemekListesi")
        self.root.geometry("600x600")

        # Renk paleti
        self.bg_color = "#2C3E50"       # Ana arka plan rengi
        self.fg_color = "#ECF0F1"       # Ana metin rengi
        self.entry_bg = "#34495E"       # Giriş alanlarının arka plan rengi
        self.button_bg = "#1ABC9C"      # Butonların arka plan rengi
        self.listbox_bg = "#34495E"     # Liste kutularının arka plan rengi
        self.highlight_bg = "#16A085"   # Seçili öğelerin arka plan rengi
        self.font = ("Arial", 12)

        self.create_widgets()

    def create_widgets(self):
        # Üst çerçeve
        frame_top = tk.Frame(self.root, pady=10, bg=self.bg_color)
        frame_top.pack(fill=tk.X)

        # İşçi ekleme arayüzü
        self.name_label = tk.Label(frame_top, text="İşçi İsmi:", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.name_label.pack(side=tk.LEFT, padx=(20, 10))

        self.name_entry = tk.Entry(frame_top, font=self.font, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color)
        self.name_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.type_label = tk.Label(frame_top, text="Tipi:", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.type_label.pack(side=tk.LEFT, padx=(20, 10))

        self.type_var = tk.StringVar(value="İşçi")
        self.type_optionmenu = tk.OptionMenu(frame_top, self.type_var, "İşçi", "Memur")
        self.type_optionmenu.config(font=self.font, bg=self.entry_bg, fg=self.fg_color)
        self.type_optionmenu.pack(side=tk.LEFT, padx=(0, 10))

        self.add_button = tk.Button(frame_top, text="İşçi Ekleme", command=self.add_worker, font=self.font, bg=self.button_bg, fg=self.bg_color)
        self.add_button.pack(side=tk.LEFT, padx=(0, 20))

        self.delete_button = tk.Button(frame_top, text="İşçi Sil", command=self.delete_worker, font=self.font, bg=self.button_bg, fg=self.bg_color)
        self.delete_button.pack(side=tk.LEFT, padx=(0, 20))

        # Orta çerçeve
        frame_middle = tk.Frame(self.root, pady=10, bg=self.bg_color)
        frame_middle.pack(fill=tk.X)

        self.list_workers_button = tk.Button(frame_middle, text="İşçi Listele", command=self.list_workers, font=self.font, bg=self.button_bg, fg=self.bg_color)
        self.list_workers_button.pack(side=tk.LEFT, padx=(20, 10))

        self.worker_listbox = tk.Listbox(frame_middle, font=self.font, bg=self.listbox_bg, fg=self.fg_color, selectbackground=self.highlight_bg, height=10)
        self.worker_listbox.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        self.worker_listbox.bind('<<ListboxSelect>>', self.on_worker_select)

        self.export_button = tk.Button(frame_middle, text="Excel'e Aktar", command=self.export_to_excel, font=self.font, bg=self.button_bg, fg=self.bg_color)
        self.export_button.pack(side=tk.LEFT, padx=(0, 20))

        # Yemek ekleme arayüzü
        frame_bottom = tk.Frame(self.root, pady=10, bg=self.bg_color)
        frame_bottom.pack(fill=tk.X)

        self.meal_amount_label = tk.Label(frame_bottom, text="Yemek Miktarı:", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.meal_amount_label.pack(side=tk.LEFT, padx=(20, 10))

        self.meal_amount_entry = tk.Entry(frame_bottom, font=self.font, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color)
        self.meal_amount_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.meal_date_label = tk.Label(frame_bottom, text="Tarih Seçimi:", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.meal_date_label.pack(side=tk.LEFT, padx=(20, 10))

        self.meal_date_entry = DateEntry(frame_bottom, font=self.font, bg=self.entry_bg, fg=self.fg_color, date_pattern='yyyy-mm-dd')
        self.meal_date_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.add_meal_button = tk.Button(frame_bottom, text="Yemek Tutarı ekle", command=self.add_meal, font=self.font, bg=self.button_bg, fg=self.bg_color)
        self.add_meal_button.pack(side=tk.LEFT, padx=(0, 20))

        # İşçi yemek bilgilerini listeleme arayüzü
        frame_meals = tk.Frame(self.root, pady=10, bg=self.bg_color)
        frame_meals.pack(fill=tk.BOTH, expand=True)

        self.meal_listbox = tk.Listbox(frame_meals, font=self.font, bg=self.listbox_bg, fg=self.fg_color, selectbackground=self.highlight_bg, height=10)
        self.meal_listbox.pack(side=tk.LEFT, padx=(20, 10), fill=tk.BOTH, expand=True)

        # Toplam yemek miktarı arayüzü
        self.total_meal_label = tk.Label(self.root, text="", font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.total_meal_label.pack(pady=(10, 20))

        # Arka plan rengi ayarları
        self.root.configure(bg=self.bg_color)

    def add_worker(self):
        name = self.name_entry.get()
        worker_type = self.type_var.get()
        if name and worker_type:
            try:
                conn = sqlite3.connect(resource_path('workers.db'))
                c = conn.cursor()
                c.execute("INSERT INTO workers (name, type) VALUES (?, ?)", (name, worker_type))
                conn.commit()
                conn.close()
                messagebox.showinfo("Başarılı", "İşçi Başarıyla Eklendi.")
                self.name_entry.delete(0, tk.END)
                self.list_workers()
            except sqlite3.Error as e:
                messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
            except Exception as e:
                messagebox.showerror("Hata", f"Beklenmeyen hata: {e}")
        else:
            messagebox.showerror("Hata", "İşçi İsmi ve tipi bulunamadı.")

    def delete_worker(self):
        try:
            worker_id = int(self.worker_listbox.get(tk.ACTIVE).split(':')[0])
            conn = sqlite3.connect(resource_path('workers.db'))
            c = conn.cursor()
            c.execute("DELETE FROM workers WHERE id = ?", (worker_id,))
            c.execute("DELETE FROM meals WHERE worker_id = ?", (worker_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Başarılı", "İşçi ve ilgili yemek bilgileri başarıyla silindi.")
            self.list_workers()
            self.meal_listbox.delete(0, tk.END)
            self.total_meal_label.config(text="")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def list_workers(self):
        self.worker_listbox.delete(0, tk.END)
        try:
            conn = sqlite3.connect(resource_path('workers.db'))
            c = conn.cursor()
            c.execute("SELECT * FROM workers")
            workers = c.fetchall()
            for worker in workers:
                self.worker_listbox.insert(tk.END, f"{worker[0]}: {worker[1]} ({worker[2]})")
            conn.close()
        except Exception as e:
            messagebox.showerror("Hata", f"İşçileri listelerken bir hata oluştu: {e}")

    def add_meal(self):
        try:
            worker_id = int(self.worker_listbox.get(tk.ACTIVE).split(':')[0])
            meal_date = self.meal_date_entry.get_date().strftime('%Y-%m-%d')
            meal_amount = float(self.meal_amount_entry.get())
            conn = sqlite3.connect(resource_path('workers.db'))
            c = conn.cursor()
            c.execute("INSERT INTO meals (worker_id, date, meal_amount) VALUES (?, ?, ?)",
                      (worker_id, meal_date, meal_amount))
            conn.commit()
            conn.close()
            messagebox.showinfo("Başarılı", "Yemek Başarıyla Eklendi.")
            self.meal_amount_entry.delete(0, tk.END)
            self.list_meals(worker_id)  # Yemek ekledikten sonra yemekleri güncelle
            self.total_meals(worker_id)
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz Giriş: {e}")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def on_worker_select(self, event):
        selected_worker = self.worker_listbox.curselection()
        if selected_worker:
            worker_id = int(self.worker_listbox.get(selected_worker).split(':')[0])
            self.total_meals(worker_id)
            self.list_meals(worker_id)

    def total_meals(self, worker_id):
        try:
            conn = sqlite3.connect(resource_path('workers.db'))
            c = conn.cursor()
            # Toplam yemek miktarını hesapla
            c.execute("SELECT SUM(meal_amount) FROM meals WHERE worker_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')", (worker_id,))
            total = c.fetchone()[0]
            # Kaç gün yemek yendiğini hesapla
            c.execute("SELECT COUNT(DISTINCT date) FROM meals WHERE worker_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')", (worker_id,))
            days = c.fetchone()[0]
            conn.close()
            if total is not None:
                self.total_meal_label.config(text=f"Bu ayki toplam yemek: {total} TL üzerinde {days} gün")
            else:
                self.total_meal_label.config(text="Bu ay için kayıtlı yemek yok.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def list_meals(self, worker_id):
        self.meal_listbox.delete(0, tk.END)
        try:
            conn = sqlite3.connect(resource_path('workers.db'))
            c = conn.cursor()
            c.execute("SELECT date, meal_amount FROM meals WHERE worker_id = ? ORDER BY date", (worker_id,))
            meals = c.fetchall()
            conn.close()
            for meal in meals:
                self.meal_listbox.insert(tk.END, f"{meal[0]}: {meal[1]}")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def export_to_excel(self):
        try:
            conn = sqlite3.connect(resource_path('workers.db'))
            workers_df = pd.read_sql_query("SELECT * FROM workers", conn)
            meals_df = pd.read_sql_query("SELECT * FROM meals", conn)
            conn.close()

            # İşçilerin ve memurların bilgilerini Excel dosyasına yaz
            with pd.ExcelWriter('workers_meals.xlsx') as writer:
                workers_df.to_excel(writer, sheet_name='Workers', index=False)
                meals_df.to_excel(writer, sheet_name='Meals', index=False)

            messagebox.showinfo("Başarılı", "Veriler başarıyla Excel dosyasına aktarıldı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkerApp(root)
    root.mainloop()
