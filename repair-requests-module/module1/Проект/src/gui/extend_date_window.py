import customtkinter as ctk

class ExtendDateWindow(ctk.CTkToplevel):
    def __init__(self, parent, current_date):
        super().__init__(parent)
        self.title("Изменение срока")
        self.geometry("300x200")
        self.result = None
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Новая дата (ГГГГ-ММ-ДД):").pack(pady=10)
        self.date_entry = ctk.CTkEntry(self, placeholder_text=current_date)
        self.date_entry.insert(0, current_date)
        self.date_entry.pack(pady=10)

        ctk.CTkButton(self, text="Сохранить", command=self._confirm).pack(pady=10)

    def _confirm(self):
        self.result = self.date_entry.get()
        self.destroy()