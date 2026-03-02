import tkinter as tk
from tkinter import ttk, messagebox


class MainWindow(tk.Tk):
    def __init__(self, requests_list):
        super().__init__()
        self.title("ООО 'БытСервис' — Учет заявок")
        self.geometry("900x500")
        self.requests = requests_list

        style = ttk.Style()
        style.theme_use('vista')

        self._create_widgets()

    def _create_widgets(self):
        label = tk.Label(self, text="Список заявок на ремонт", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        columns = ("id", "date", "tech", "model", "status")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        self.tree.heading("id", text="№")
        self.tree.heading("date", text="Дата")
        self.tree.heading("tech", text="Техника")
        self.tree.heading("model", text="Модель")
        self.tree.heading("status", text="Статус")

        for req in self.requests:
            self.tree.insert("", tk.END, values=(
                req.request_id,
                req.start_date.strftime('%Y-%m-%d'),
                req.tech_type,
                req.tech_model,
                req.status
            ))

        self.tree.pack(expand=True, fill='both', padx=20, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        edit_btn = tk.Button(btn_frame, text="Редактировать заявку", command=self._edit_request)
        edit_btn.pack(side=tk.LEFT, padx=10)

        stats_btn = tk.Button(btn_frame, text="Показать статистику", command=self._show_stats)
        stats_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(btn_frame, text="Выход", command=self.destroy)
        exit_btn.pack(side=tk.LEFT, padx=10)

    def _edit_request(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заявку из списка!", icon="warning")  # Уведомление по ТЗ
            return
        messagebox.showinfo("Инфо", "Окно редактирования в разработке")

    def _show_stats(self):
        messagebox.showinfo("Статистика", "Здесь будет расчет среднего времени ремонта")