import tkinter as tk
from tkinter import ttk, messagebox


class EditWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.title(f"Редактирование заявки №{request.request_id}")
        self.geometry("400x450")
        self.request = request
        self.result = None

        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="Описание проблемы:").pack(pady=5)
        self.desc_text = tk.Text(self, height=4, width=40)
        self.desc_text.insert("1.0", self.request.problem)
        self.desc_text.pack(pady=5)

        tk.Label(self, text="Статус заявки:").pack(pady=5)
        self.status_cb = ttk.Combobox(self, values=[
            "новая заявка",
            "в процессе ремонта",
            "ожидание запчастей",
            "готова к выдаче"
        ])
        self.status_cb.set(self.request.status)
        self.status_cb.pack(pady=5)

        tk.Label(self, text="Комментарий мастера / Запчасти:").pack(pady=5)
        self.comment_entry = tk.Entry(self, width=40)
        self.comment_entry.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Сохранить", command=self._save).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def _save(self):
        if not self.status_cb.get():
            messagebox.showerror("Ошибка", "Статус должен быть выбран!", icon="error")
            return

        if messagebox.askyesno("Подтверждение", "Сохранить изменения в заявке?"):
            self.request.status = self.status_cb.get()
            self.request.problem = self.desc_text.get("1.0", tk.END).strip()
            new_comment = self.comment_entry.get().strip()
            if new_comment:
                self.new_comment_text = new_comment  # Сохраняем для передачи в main_window

            self.result = self.request
            self.destroy()