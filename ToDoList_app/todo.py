import tkinter as tk
from tkinter import messagebox
import sqlite3

# Veritabanı bağlantısı
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0
)
""")
conn.commit()

# Ana uygulama penceresi
root = tk.Tk()
root.title("To-Do Uygulaması")
root.geometry("400x400")

# Görevleri listele
def list_tasks():
    task_list.delete(0, tk.END)
    cursor.execute("SELECT id, description, completed FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        status = "✅" if task[2] else "❌"
        task_list.insert(tk.END, f"{task[0]}. {task[1]} [{status}]")

# Görev ekle
def add_task():
    description = entry.get()
    if description.strip() == "":
        messagebox.showwarning("Uyarı", "Lütfen görev girin.")
        return
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
    conn.commit()
    entry.delete(0, tk.END)
    list_tasks()

# Görevi tamamla
def complete_task():
    selected = task_list.curselection()
    if not selected:
        return
    task_text = task_list.get(selected[0])
    task_id = int(task_text.split('.')[0])
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    list_tasks()

# Görevi sil
def delete_task():
    selected = task_list.curselection()
    if not selected:
        return
    task_text = task_list.get(selected[0])
    task_id = int(task_text.split('.')[0])
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    list_tasks()

# Arayüz bileşenleri
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

add_button = tk.Button(root, text="Görev Ekle", command=add_task)
add_button.pack()

task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)

complete_button = tk.Button(root, text="Tamamlandı Olarak İşaretle", command=complete_task)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Görevi Sil", command=delete_task)
delete_button.pack(pady=5)

list_tasks()  # İlk açılışta görevleri yükle

root.mainloop()
conn.close()
