import tkinter as tk
from tkinter import messagebox
from auth import AuthService


class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")
        self.root.geometry("300x200")

        self.auth_service = AuthService()

        self.label_login = tk.Label(root, text="Логин")
        self.label_login.pack()

        self.entry_login = tk.Entry(root)
        self.entry_login.pack()

        self.label_password = tk.Label(root, text="Пароль")
        self.label_password.pack()

        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(root, text="Войти", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showerror(
                "Ошибка",
                "Введите логин и пароль"
            )
            return

        user = self.auth_service.authenticate(login, password)

        if user is None:
            messagebox.showerror(
                "Ошибка авторизации",
                "Неверный логин или пароль"
            )
        else:
            messagebox.showinfo(
                "Успешный вход",
                f"Добро пожаловать, {user['role']}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()