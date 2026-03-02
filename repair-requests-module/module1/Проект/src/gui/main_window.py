import tkinter as tk
from tkinter import ttk, messagebox
from gui.edit_window import EditWindow

class MainWindow(tk.Tk):
    def __init__(self, requests_list, current_user):
        super().__init__()
        self.title(f"ООО 'БытСервис' — {current_user['fio']} ({current_user['type']})")
        self.geometry("900(x)550")
        self.requests = requests_list
        self.user = current_user # Сохраняем данные вошедшего пользователя

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

        if self.user['type'] in ["Оператор", "Мастер"]:
            tk.Button(btn_frame, text="Редактировать заявку",
                      command=self._edit_request).pack(side=tk.LEFT, padx=10)

        if self.user['type'] == "Менеджер":
            tk.Button(btn_frame, text="Отчет по статистике",
                      command=self._show_stats).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Выход", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def _show_stats(self):
        completed = [r for r in self.requests if r.status == "Готова к выдаче"]
        count = len(completed)
        messagebox.showinfo("Статистика", f"Выполнено заявок: {count}", icon="info")

    def _edit_request(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заявку для редактирования!", icon="warning")
            return

        item_id = self.tree.item(selected)['values'][0]
        request_to_edit = next((r for r in self.requests if str(r.request_id) == str(item_id)), None)

        if request_to_edit:
            edit_win = EditWindow(self, request_to_edit)
            self.wait_window(edit_win)

            if edit_win.result:
                self._refresh_table()

    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for req in self.requests:
            self.tree.insert("", tk.END, values=(
                req.request_id, req.start_date, req.tech_type, req.tech_model, req.status
            ))