import tkinter as tk
from tkinter import messagebox
from auth import AuthService
from services import RequestService


class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")
        self.root.geometry("300x200")

        self.auth_service = AuthService()

        tk.Label(root, text="Логин").pack()
        self.entry_login = tk.Entry(root)
        self.entry_login.pack()

        tk.Label(root, text="Пароль").pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        tk.Button(root, text="Войти", command=self.login).pack(pady=10)

    def login(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
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
        self.request_service = RequestService()

        self.root.title("Главное меню")
        self.root.geometry("400x300")

        tk.Label(
            root,
            text=f"Вы вошли как: {user['role']}",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            root,
            text="Добавить заявку",
            width=25,
            command=self.open_add_window
        ).pack(pady=5)

        tk.Button(
            root,
            text="Просмотр заявок",
            width=25,
            command=self.open_view_window
        ).pack(pady=5)

        tk.Button(
            root,
            text="Статистика",
            width=25,
            command=self.not_implemented
        ).pack(pady=5)

        tk.Button(
            root,
            text="Выход",
            width=25,
            command=self.root.quit
        ).pack(pady=20)

    def not_implemented(self):
        messagebox.showinfo(
            "Информация",
            "Функция будет реализована далее"
        )

    def open_add_window(self):
        AddRequestWindow(self.root, self.request_service)

    def open_view_window(self):
        ViewRequestsWindow(self.root, self.request_service)


class AddRequestWindow:

    def __init__(self, parent, request_service):
        self.request_service = request_service

        self.window = tk.Toplevel(parent)
        self.window.title("Добавление заявки")
        self.window.geometry("400x400")

        tk.Label(self.window, text="Вид техники").pack()
        self.entry_device = tk.Entry(self.window)
        self.entry_device.pack()

        tk.Label(self.window, text="Модель").pack()
        self.entry_model = tk.Entry(self.window)
        self.entry_model.pack()

        tk.Label(self.window, text="Описание проблемы").pack()
        self.entry_problem = tk.Entry(self.window)
        self.entry_problem.pack()

        tk.Label(self.window, text="ФИО клиента").pack()
        self.entry_client = tk.Entry(self.window)
        self.entry_client.pack()

        tk.Label(self.window, text="Телефон").pack()
        self.entry_phone = tk.Entry(self.window)
        self.entry_phone.pack()

        tk.Button(
            self.window,
            text="Сохранить",
            command=self.save_request
        ).pack(pady=10)

    def save_request(self):
        device = self.entry_device.get()
        model = self.entry_model.get()
        problem = self.entry_problem.get()
        client = self.entry_client.get()
        phone = self.entry_phone.get()

        if not device or not model or not problem or not client or not phone:
            messagebox.showerror(
                "Ошибка",
                "Все поля должны быть заполнены"
            )
            return

        self.request_service.add_request(
            device,
            model,
            problem,
            client,
            phone
        )

        messagebox.showinfo(
            "Успешно",
            "Заявка успешно добавлена"
        )

        self.window.destroy()


class ViewRequestsWindow:

    def __init__(self, parent, request_service):
        self.request_service = request_service

        self.window = tk.Toplevel(parent)
        self.window.title("Просмотр заявок")
        self.window.geometry("700x400")

        headers = ["ID", "Дата", "Техника", "Модель", "Описание", "Клиент", "Телефон", "Статус"]
        for idx, h in enumerate(headers):
            tk.Label(self.window, text=h, borderwidth=1, relief="solid", width=12).grid(row=0, column=idx)

        for row_idx, req in enumerate(self.request_service.get_all_requests(), start=1):
            tk.Label(self.window, text=req.request_id, borderwidth=1, relief="solid").grid(row=row_idx, column=0)
            tk.Label(self.window, text=req.date_added.strftime("%d.%m.%Y %H:%M"), borderwidth=1, relief="solid").grid(row=row_idx, column=1)
            tk.Label(self.window, text=req.device_type, borderwidth=1, relief="solid").grid(row=row_idx, column=2)
            tk.Label(self.window, text=req.model, borderwidth=1, relief="solid").grid(row=row_idx, column=3)
            tk.Label(self.window, text=req.problem_description, borderwidth=1, relief="solid").grid(row=row_idx, column=4)
            tk.Label(self.window, text=req.client_name, borderwidth=1, relief="solid").grid(row=row_idx, column=5)
            tk.Label(self.window, text=req.phone, borderwidth=1, relief="solid").grid(row=row_idx, column=6)
            tk.Label(self.window, text=req.status, borderwidth=1, relief="solid").grid(row=row_idx, column=7)


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()