import customtkinter as ctk
import os
from tkinter import messagebox
from utils.csv_handler import load_users


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Находим корень проекта
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.users = load_users(self.project_root)
        self.authorized_user = None

        # Настройки окна
        self.title("Авторизация — ООО 'БытСервис'")
        self.geometry("400x350")
        self.resizable(False, False)

        # Центрируем окно на экране
        self.eval('tk::PlaceWindow . center')

        self._create_widgets()

    def _create_widgets(self):
        # Заголовок
        self.label = ctk.CTkLabel(self, text="Вход в систему", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(30, 20))

        # Поле логина
        self.login_entry = ctk.CTkEntry(self, placeholder_text="Логин", width=280, height=40)
        self.login_entry.pack(pady=10)

        # Поле пароля
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Пароль", width=280, height=40, show="*")
        self.password_entry.pack(pady=10)

        # Контейнер для кнопок
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=30)

        # Кнопка Войти
        self.login_button = ctk.CTkButton(self.btn_frame, text="Войти", width=130, height=35,
                                          command=self._authenticate)
        self.login_button.pack(side="left", padx=10)

        # Кнопка Отмена
        self.cancel_button = ctk.CTkButton(self.btn_frame, text="Отмена", width=130, height=35,
                                           fg_color="#444444", hover_color="#333333",
                                           command=self.destroy)
        self.cancel_button.pack(side="left", padx=10)

        # Привязка клавиши Enter для быстрого входа
        self.bind('<Return>', lambda event: self._authenticate())

    def _authenticate(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Ищем пользователя в загруженном списке
        user = next((u for u in self.users if u['login'] == login and u['password'] == password), None)

        if user:
            # Успех
            self.authorized_user = user
            # Мы не вызываем messagebox здесь, чтобы не портить вид,
            # либо используем стандартный, если нужно подтверждение.
            self.quit()
            self.destroy()
        else:
            # Ошибка
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.login_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.login_entry.focus()