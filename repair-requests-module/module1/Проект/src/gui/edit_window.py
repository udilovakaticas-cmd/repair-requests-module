import customtkinter as ctk
from tkinter import messagebox


class EditWindow(ctk.CTkToplevel):
    def __init__(self, parent, request):
        super().__init__(parent)

        self.request = request
        self.result = None

        self.title(f"Редактирование заявки №{request.request_id}")
        self.geometry("450x550")

        # Поверх всех окон
        self.attributes("-topmost", True)

        # Чтобы вставка работала (прокидываем глобальную функцию из main)
        # Если вызываешь из MainWindow, shortcuts применятся автоматически через bind_class

        self._create_widgets()

    def _create_widgets(self):
        # Заголовок окна
        self.header = ctk.CTkLabel(self, text=f"Заявка #{self.request.request_id}",
                                   font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=15)

        # Описание проблемы
        ctk.CTkLabel(self, text="Описание проблемы:", font=("Arial", 12)).pack(anchor="w", padx=40)
        self.desc_text = ctk.CTkTextbox(self, height=100, width=370, border_width=2)
        self.desc_text.insert("1.0", self.request.problem)
        self.desc_text.pack(pady=(5, 15))

        # Статус заявки
        ctk.CTkLabel(self, text="Статус заявки:", font=("Arial", 12)).pack(anchor="w", padx=40)
        self.status_cb = ctk.CTkComboBox(self, width=370, values=[
            "новая заявка",
            "в процессе ремонта",
            "ожидание запчастей",
            "готова к выдаче"
        ])
        self.status_cb.set(self.request.status)
        self.status_cb.pack(pady=(5, 15))

        # Комментарий мастера / Запчасти
        ctk.CTkLabel(self, text="Комментарий / Запчасти:", font=("Arial", 12)).pack(anchor="w", padx=40)
        self.comment_entry = ctk.CTkEntry(self, width=370, placeholder_text="Введите примечание...")
        self.comment_entry.pack(pady=(5, 15))

        # Кнопки
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.save_btn = ctk.CTkButton(self.btn_frame, text="Сохранить", fg_color="#2ecc71",
                                      hover_color="#27ae60", width=120, command=self._save)
        self.save_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(self.btn_frame, text="Отмена", fg_color="#e74c3c",
                                        hover_color="#c0392b", width=120, command=self.destroy)
        self.cancel_btn.pack(side="left", padx=10)

    def _save(self):
        current_status = self.status_cb.get()
        if not current_status:
            messagebox.showerror("Ошибка", "Выберите статус!")
            return

        if messagebox.askyesno("Подтверждение", f"Сохранить изменения для заявки №{self.request.request_id}?"):
            # Обновляем объект заявки
            self.request.status = current_status
            self.request.problem = self.desc_text.get("1.0", "end").strip()

            new_comment = self.comment_entry.get().strip()
            if new_comment:
                self.new_comment_text = new_comment

            self.result = self.request  # Передаем результат обратно в MainWindow
            self.destroy()