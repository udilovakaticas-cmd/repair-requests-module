import os
import sys
from utils.csv_handler import load_all_data
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from tkinter import messagebox


def main():
    # Находим корень проекта (папка "Проект")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # 1. Сначала логин
    login_app = LoginWindow()
    login_app.mainloop()

    # 2. Если вошли успешно
    if hasattr(login_app, 'authorized_user') and login_app.authorized_user:
        user_data = login_app.authorized_user

        # Загружаем данные, используя корень проекта
        requests_list = load_all_data(project_root)

        try:
            # ТУТ ИСПРАВЛЕНИЕ: передаем и список, и пользователя
            app = MainWindow(requests_list, user_data)
            app.mainloop()
        except Exception as ex:
            messagebox.showerror("Критический сбой", f"Ошибка: {ex}")
    else:
        print("Вход не выполнен.")


if __name__ == "__main__":
    main()