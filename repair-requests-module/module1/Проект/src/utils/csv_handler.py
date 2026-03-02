import csv
import os
from tkinter import messagebox
from models.request import RepairRequest


def load_all_data(base_path):

    requests = []
    req_file = os.path.join(base_path, '..', 'data', 'inputDataRequests.csv')

    try:
        if not os.path.exists(req_file):
            messagebox.showwarning("Файл не найден", f"Файл {req_file} отсутствует.", icon="warning")
            return requests

        with open(req_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                requests.append(RepairRequest(row))
    except Exception as e:
        messagebox.showerror("Ошибка загрузки", f"Не удалось прочитать данные: {str(e)}", icon="error")

    return requests


def load_users(base_path):
    user_file = os.path.join(base_path, '..', 'data', 'inputDataUsers.csv')
    users = []
    try:
        with open(user_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                users.append(row)
    except Exception as e:
        messagebox.showerror("Ошибка пользователей", f"Ошибка доступа к списку пользователей: {e}")
    return users