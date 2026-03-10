import customtkinter as ctk
from datetime import datetime

class CreateRequestWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Подача новой заявки")
        self.geometry("400x450")
        self.result = None
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text="Новая заявка", font=("Arial", 20, "bold")).pack(pady=20)

        self.tech_type = ctk.CTkEntry(self, placeholder_text="Тип техники (например, Холодильник)", width=300)
        self.tech_type.pack(pady=10)

        self.tech_model = ctk.CTkEntry(self, placeholder_text="Модель", width=300)
        self.tech_model.pack(pady=10)

        self.problem = ctk.CTkTextbox(self, width=300, height=100)
        self.problem.insert("1.0", "Описание проблемы...")
        self.problem.pack(pady=10)

        ctk.CTkButton(self, text="Отправить заявку", fg_color="green", command=self._save).pack(pady=20)

    def _save(self):
        self.result = {
            'tech_type': self.tech_type.get(),
            'tech_model': self.tech_model.get(),
            'problem': self.problem.get("1.0", "end").strip()
        }
        self.destroy()