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
            self.root.destroy()
            main_root = tk.Tk()
            MainWindow(main_root, user)
            main_root.mainloop()


class MainWindow:

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Главное меню")
        self.root.geometry("400x300")

        self.label_title = tk.Label(
            root,
            text=f"Вы вошли как: {user['role']}",
            font=("Arial", 12)
        )
        self.label_title.pack(pady=10)

        self.button_add = tk.Button(
            root,
            text="Добавить заявку",
            width=25,
            command=self.not_implemented
        )
        self.button_add.pack(pady=5)

        self.button_view = tk.Button(
            root,
            text="Просмотр заявок",
            width=25,
            command=self.not_implemented
        )
        self.button_view.pack(pady=5)

        self.button_stats = tk.Button(
            root,
            text="Статистика",
            width=25,
            command=self.not_implemented
        )
        self.button_stats.pack(pady=5)

        self.button_exit = tk.Button(
            root,
            text="Выход",
            width=25,
            command=self.root.quit
        )
        self.button_exit.pack(pady=20)

    def not_implemented(self):
        messagebox.showinfo(
            "Информация",
            "Функция будет реализована далее"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()