import customtkinter as ctk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from gui.edit_window import EditWindow
from gui.assign_window import AssignMasterWindow
from gui.create_request_window import CreateRequestWindow
from gui.extend_date_window import ExtendDateWindow
from utils.csv_handler import load_users, get_project_root, save_requests, show_feedback_qr


class MainWindow(ctk.CTk):
    def __init__(self, requests_list, current_user):
        super().__init__()
        self.requests = requests_list
        self.user = current_user

        self.title(f"БытСервис — {self.user['fio']} ({self.user['type']})")
        self.geometry("1100x600")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковое меню
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="МЕНЮ", font=("Arial", 20, "bold")).pack(pady=20)

        # РАСПРЕДЕЛЕНИЕ КНОПОК ПО ТЗ
        if self.user['type'] == "Менеджер":
            ctk.CTkButton(self.sidebar, text="Назначить мастера", command=self._assign_master).pack(pady=10, padx=20)
            ctk.CTkButton(self.sidebar, text="Статистика", command=self._show_stats).pack(pady=10, padx=20)

        elif self.user['type'] == "Заказчик":
            ctk.CTkButton(self.sidebar, text="Новая заявка", fg_color="green", command=self._create_new_request).pack(
                pady=10, padx=20)
            ctk.CTkButton(self.sidebar, text="Изменить описание", command=self._edit_request).pack(pady=10, padx=20)

        elif self.user['type'] == "Мастер":
            ctk.CTkButton(self.sidebar, text="Отчет / Запчасти", command=self._edit_request).pack(pady=10, padx=20)

        elif self.user['type'] == "Менеджер по качеству":
            ctk.CTkButton(self.sidebar, text="Продлить срок", fg_color="darkorange", command=self._extend_date).pack(
                pady=10, padx=20)
            ctk.CTkButton(self.sidebar, text="Переназначить", command=self._assign_master).pack(pady=10, padx=20)

        # Кнопка QR (видна всем, но логика внутри)
        ctk.CTkButton(self.sidebar, text="QR-отзыв", command=self._open_qr).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Выход", fg_color="#a93226", command=self.quit).pack(side="bottom", pady=20,
                                                                                              padx=20)

        # Таблица
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.tree = ttk.Treeview(self.container, columns=("id", "date", "tech", "status", "master"), show='headings')
        for col, text in zip(("id", "date", "tech", "status", "master"), ("№", "Дата", "Техника", "Статус", "Мастер")):
            self.tree.heading(col, text=text)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self._refresh_table()

    def _refresh_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for req in self.requests:
            # Мастер видит только СВОИ
            if self.user['type'] == "Мастер" and str(req.master_id) != str(self.user['userID']):
                continue
            # Заказчик видит только СВОИ
            if self.user['type'] == "Заказчик" and str(req.client_id) != str(self.user['userID']):
                continue

            self.tree.insert("", "end",
                             values=(req.request_id, req.start_date, req.tech_type, req.status, req.master_id))

    def _create_new_request(self):
        win = CreateRequestWindow(self)
        self.wait_window(win)
        if win.result:
            from models.request import RepairRequest
            new_id = max([int(r.request_id) for r in self.requests]) + 1 if self.requests else 1
            data = {
                'requestID': str(new_id), 'startDate': datetime.now().strftime("%Y-%m-%d"),
                'homeTechType': win.result['tech_type'], 'homeTechModel': win.result['tech_model'],
                'problemDescryption': win.result['problem'], 'requestStatus': 'новая заявка',
                'masterID': '0', 'clientID': self.user['userID'], 'completionDate': '', 'repairParts': ''
            }
            self.requests.append(RepairRequest(data))
            save_requests(self.requests)
            self._refresh_table()

    def _extend_date(self):
        selected = self.tree.selection()
        if not selected: return messagebox.showwarning("!", "Выберите заявку")
        req_id = self.tree.item(selected)['values'][0]
        req = next(r for r in self.requests if str(r.request_id) == str(req_id))

        win = ExtendDateWindow(self, getattr(req, 'completion_date', ''))
        self.wait_window(win)
        if win.result:
            req.completion_date = win.result
            save_requests(self.requests)
            messagebox.showinfo("Успех", "Дата изменена")

    def _open_qr(self):
        selected = self.tree.selection()
        if not selected: return messagebox.showwarning("!", "Выберите заявку")
        status = self.tree.item(selected)['values'][3]

        if status == "готова к выдаче" or self.user['type'] != "Заказчик":
            show_feedback_qr()
        else:
            messagebox.showwarning("Рано!", "QR-код доступен только после завершения ремонта")

    # Метод статистики (для Менеджера)
    def _show_stats(self):
        done = len([r for r in self.requests if r.status == "готова к выдаче"])
        messagebox.showinfo("Статистика", f"Завершено: {done} из {len(self.requests)}")

    # Метод назначения мастера (Менеджер / Менеджер по качеству)
    def _assign_master(self):
        selected = self.tree.selection()
        if not selected: return messagebox.showwarning("!", "Выберите заявку")
        req_id = self.tree.item(selected)['values'][0]
        req = next(r for r in self.requests if str(r.request_id) == str(req_id))

        users = load_users(get_project_root())
        win = AssignMasterWindow(self, req, users)
        self.wait_window(win)
        if win.result:
            save_requests(self.requests)
            self._refresh_table()

    def _edit_request(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return messagebox.showwarning("Внимание", "Выберите заявку в таблице!")

        # 1. Получаем ID заявки из выбранной строки
        req_id = self.tree.item(selected_item)['values'][0]
        # 2. Находим объект заявки в общем списке
        req = next((r for r in self.requests if str(r.request_id) == str(req_id)), None)

        if req:
            # ПРОВЕРКА ДЛЯ ЗАКАЗЧИКА (из ТЗ):
            if self.user['type'] == "Заказчик" and req.status != "новая заявка":
                return messagebox.showerror("Ошибка", "Нельзя редактировать заявку, которая уже находится в работе!")

            # 3. Открываем окно редактирования
            edit_win = EditWindow(self, req)
            self.wait_window(edit_win) # Ждем, пока пользователь закроет окно

            # 4. Если в окне нажали "Сохранить" (result будет содержать объект)
            if edit_win.result:
                # Если мастер добавил комментарий, сохраняем его
                if hasattr(edit_win, 'new_comment_text') and edit_win.new_comment_text:
                    from utils.csv_handler import save_comment
                    save_comment(req.request_id, edit_win.new_comment_text, self.user['userID'])

                # Сохраняем все изменения в основной файл заявок
                if save_requests(self.requests):
                    self._refresh_table()
                    messagebox.showinfo("Успех", "Изменения успешно сохранены!")