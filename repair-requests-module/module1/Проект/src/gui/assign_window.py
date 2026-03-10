import customtkinter as ctk


class AssignMasterWindow(ctk.CTkToplevel):
    def __init__(self, parent, request, users_list):
        super().__init__(parent)
        self.parent = parent
        self.request = request
        self.result = None

        self.title("Назначение мастера")
        self.geometry("400x300")
        self.attributes("-topmost", True)  # Окно поверх всех

        # Фильтруем только мастеров из списка пользователей
        self.masters = [u for u in users_list if u['type'] == "Мастер"]
        self.master_names = [m['fio'] for m in self.masters]

        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self, text=f"Заявка №{self.request.request_id}",
                     font=("Arial", 16, "bold")).pack(pady=15)

        ctk.CTkLabel(self, text="Выберите мастера из списка:").pack(pady=5)

        self.combo = ctk.CTkComboBox(self, values=self.master_names, width=250)
        self.combo.pack(pady=10)

        if self.master_names:
            self.combo.set(self.master_names[0])

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Назначить", fg_color="green",
                      command=self._save).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Отмена", fg_color="gray",
                      command=self.destroy).pack(side="left", padx=10)

    def _save(self):
        selected_fio = self.combo.get()
        # Находим объект выбранного мастера, чтобы получить его ID
        selected_master = next((m for m in self.masters if m['fio'] == selected_fio), None)

        if selected_master:
            self.request.master_id = selected_master['userID']
            # Сохраняем имя для отображения в таблице (опционально)
            self.request.master_fio = selected_fio
            self.result = True
            self.destroy()