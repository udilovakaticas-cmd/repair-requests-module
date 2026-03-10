import os
import sys
import customtkinter as ctk  # Современные стили
from utils.csv_handler import load_all_data
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from tkinter import messagebox


def setup_global_shortcuts(root):
    """Исправляет проблему Ctrl+C / Ctrl+V для всех полей ввода"""

    def copy_text(event):
        try:
            selected_text = event.widget.selection_get()
            root.clipboard_clear()
            root.clipboard_append(selected_text)
        except:
            pass
        return "break"

    def paste_text(event):
        try:
            text = root.clipboard_get()
            event.widget.insert('insert', text)
        except:
            pass
        return "break"

    # Привязываем ко всем элементам ввода (Entry и Text)
    root.bind_class("Entry", "<Control-v>", paste_text)
    root.bind_class("Entry", "<Control-c>", copy_text)
    root.bind_class("CTkEntry", "<Control-v>", paste_text)
    root.bind_class("CTkEntry", "<Control-c>", copy_text)


def main():
    # Настройка темы приложения
    ctk.set_appearance_mode("dark")  # "dark", "light" или "system"
    ctk.set_default_color_theme("blue")  # Цветовая схема

    # Определение пути к проекту
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # 1. Запуск окна авторизации
    login_app = LoginWindow()

    # Включаем поддержку Ctrl+V в окне логина
    setup_global_shortcuts(login_app)

    # Центрируем и задаем размер
    login_app.geometry("400x350")
    login_app.mainloop()

    # Проверяем, прошла ли авторизация
    if hasattr(login_app, 'authorized_user') and login_app.authorized_user:
        user_data = login_app.authorized_user

        try:
            # Загрузка данных
            requests_list = load_all_data(project_root)

            # 2. Запуск основного окна
            app = MainWindow(requests_list, user_data)

            # Включаем поддержку Ctrl+V в основном окне
            setup_global_shortcuts(app)

            # Улучшаем отображение: открываем на весь экран, чтобы всё влезло
            app.after(0, lambda: app.state('zoomed'))
            app.title(f"Сервисный Центр — Сессия: {user_data['fio']}")

            app.mainloop()

        except Exception as ex:
            # Используем стандартный messagebox, так как он надежен для фатальных ошибок
            messagebox.showerror("Критический сбой", f"Ошибка при загрузке системы: {ex}")
    else:
        print("Вход в систему не был выполнен.")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)