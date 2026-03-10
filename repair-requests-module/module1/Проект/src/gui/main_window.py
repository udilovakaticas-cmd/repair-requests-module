import qrcode
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk


def show_feedback_qr():
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform?usp=sf_link"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    top = tk.Toplevel()
    top.title("Оцените нашу работу")

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(top, image=img_tk)
    label.image = img_tk
    label.pack(padx=20, pady=20)
    tk.Label(top, text="Отсканируйте код для отзыва").pack(pady=10)


class MainWindow(tk.Tk):
    def __init__(self, requests_list, current_user):
        super().__init__()
        self.title(f"ООО 'БытСервис' — {current_user['fio']} ({current_user['type']})")
        self.geometry("900x600")
        self.requests = requests_list
        self.user = current_user

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

        self._refresh_table()
        self.tree.pack(expand=True, fill='both', padx=20, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        if self.user['type'] in ["Оператор", "Мастер", "Менеджер по качеству"]:
            tk.Button(btn_frame, text="Редактировать заявку",
                      command=self._edit_request).pack(side=tk.LEFT, padx=10)

        if self.user['type'] == "Менеджер":
            tk.Button(btn_frame, text="Отчет по статистике",
                      command=self._show_stats).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="QR-отзыв",
                  command=show_feedback_qr, bg="#e1e1e1").pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Выход", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def _show_stats(self):
        completed = [r for r in self.requests if r.status == "Готова к выдаче"]
        count = len(completed)
        messagebox.showinfo("Статистика", f"Выполнено заявок: {count}")

    def _edit_request(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заявку!")
            return

        item_values = self.tree.item(selected)['values']
        req = next((r for r in self.requests if str(r.request_id) == str(item_values[0])), None)

        if req:
            from gui.edit_window import EditWindow
            edit_win = EditWindow(self, req)
            self.wait_window(edit_win)

            if hasattr(edit_win, 'result') and edit_win.result:
                self._refresh_table()
                messagebox.showinfo("Успех", "Данные обновлены!")

    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for req in self.requests:
            self.tree.insert("", tk.END, values=(
                req.request_id, req.start_date, req.tech_type, req.tech_model, req.status
            ))