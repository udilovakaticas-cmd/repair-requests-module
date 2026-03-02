import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from auth import AuthService
from services import RequestService, Request


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
            messagebox.showerror("Ошибка авторизации", "Неверный логин или пароль")
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
        self.root.geometry("400x350")

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
            command=self.show_statistics
        ).pack(pady=5)

        tk.Button(
            root,
            text="Выход",
            width=25,
            command=self.root.quit
        ).pack(pady=20)

    def open_add_window(self):
        AddRequestWindow(self.root, self.request_service)

    def open_view_window(self):
        ViewRequestsWindow(self.root, self.request_service)

    def show_statistics(self):
        total = len(self.request_service.get_all_requests())
        if total == 0:
            messagebox.showinfo("Статистика", "Заявок пока нет")
            return

        total_time = sum(req.time_to_complete for req in self.request_service.get_all_requests())
        avg_time = total_time / total

        messagebox.showinfo(
            "Статистика",
            f"Всего заявок: {total}\n"
            f"Среднее время выполнения: {avg_time:.1f} минут"
        )


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

        tk.Label(self.window, text="Время выполнения (мин)").pack()
        self.entry_time = tk.Entry(self.window)
        self.entry_time.pack()

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
        time_str = self.entry_time.get()

        if not all([device, model, problem, client, phone, time_str]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        try:
            time_to_complete = float(time_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Время выполнения должно быть числом")
            return

        self.request_service.add_request(
            device=device,
            model=model,
            problem=problem,
            client=client,
            phone=phone,
            time_to_complete=time_to_complete
        )

        messagebox.showinfo("Успешно", "Заявка успешно добавлена")
        self.window.destroy()


class ViewRequestsWindow:

    def __init__(self, parent, request_service):
        self.request_service = request_service

        self.window = tk.Toplevel(parent)
        self.window.title("Просмотр заявок")
        self.window.geometry("800x500")

        # Фильтр по статусу
        tk.Label(self.window, text="Фильтр по статусу:").pack(pady=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Все")
        options = ["Все", "новая заявка", "в процессе ремонта", "готова к выдаче"]
        tk.OptionMenu(self.window, self.status_var, *options, command=self.refresh_table).pack(pady=5)

        # Canvas + Scrollbar
        self.canvas = tk.Canvas(self.window)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.refresh_table()

    def refresh_table(self, *args):
        for widget in self.frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Дата", "Техника", "Модель", "Описание", "Клиент", "Телефон", "Статус", "Время мин"]
        for idx, h in enumerate(headers):
            tk.Label(self.frame, text=h, borderwidth=1, relief="solid", width=12, bg="#dddddd").grid(row=0, column=idx)

        filtered_requests = self.request_service.get_all_requests()
        status_filter = self.status_var.get()
        if status_filter != "Все":
            filtered_requests = [r for r in filtered_requests if r.status == status_filter]

        for row_idx, req in enumerate(filtered_requests, start=1):
            tk.Label(self.frame, text=req.request_id, borderwidth=1, relief="solid").grid(row=row_idx, column=0)
            tk.Label(self.frame, text=req.date_added.strftime("%d.%m.%Y %H:%M"), borderwidth=1, relief="solid").grid(row=row_idx, column=1)
            tk.Label(self.frame, text=req.device_type, borderwidth=1, relief="solid").grid(row=row_idx, column=2)
            tk.Label(self.frame, text=req.model, borderwidth=1, relief="solid").grid(row=row_idx, column=3)
            tk.Label(self.frame, text=req.problem_description, borderwidth=1, relief="solid").grid(row=row_idx, column=4)
            tk.Label(self.frame, text=req.client_name, borderwidth=1, relief="solid").grid(row=row_idx, column=5)
            tk.Label(self.frame, text=req.phone, borderwidth=1, relief="solid").grid(row=row_idx, column=6)
            tk.Label(self.frame, text=req.status, borderwidth=1, relief="solid").grid(row=row_idx, column=7)
            tk.Label(self.frame, text=req.time_to_complete, borderwidth=1, relief="solid").grid(row=row_idx, column=8)


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()