import tkinter as tk
from tkinter import messagebox
import os
from utils.csv_handler import load_users


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        self.users = load_users(self.project_root)
        self.authorized_user = None

        self.title("Авторизация — ООО 'БытСервис'")
        self.geometry("350x250")
        self.resizable(False, False)

        base_path = os.path.dirname(os.path.abspath(__file__))


        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="Вход в систему", font=("Arial", 12, "bold")).pack(pady=15)

        tk.Label(self, text="Логин:").pack()
        self.login_entry = tk.Entry(self, width=30)
        self.login_entry.pack(pady=5)

        tk.Label(self, text="Пароль:").pack()
        self.password_entry = tk.Entry(self, width=30, show="*")  # Маскировка пароля
        self.password_entry.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Войти", width=10, command=self._authenticate).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", width=10, command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _authenticate(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        user = next((u for u in self.users if u['login'] == login and u['password'] == password), None)

        if user:
            messagebox.showinfo("Успех", f"Авторизация успешна!\nЗдравствуйте, {user['fio']}")
            self.authorized_user = user
            self.quit()
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль", icon="error")