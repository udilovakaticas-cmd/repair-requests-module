import os
import sys
from utils.csv_handler import load_all_data
from gui.main_window import MainWindow
from tkinter import messagebox


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))

    requests_list = load_all_data(base_path)

    if not requests_list:
        messagebox.showinfo("Инфо", "Список заявок пуст. Добавьте первую заявку через меню.", icon="info")

    try:
        app = MainWindow(requests_list)
        app.mainloop()
    except Exception as ex:
        messagebox.showerror("Критический сбой", f"Приложение будет закрыто: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()