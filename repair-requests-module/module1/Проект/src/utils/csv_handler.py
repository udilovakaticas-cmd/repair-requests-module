import csv
import os
from tkinter import messagebox

def load_users(project_root):
    user_file = os.path.join(project_root, 'data', 'inputDataUsers.csv')
    users = []
    try:
        with open(user_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл не найден: {user_file}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка чтения пользователей: {e}")
    return users

def load_all_data(project_root):
    from models.request import RepairRequest
    req_file = os.path.join(project_root, 'data', 'inputDataRequests.csv')
    requests = []
    try:
        with open(req_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                requests.append(RepairRequest(row))
    except Exception as e:
        print(f"Ошибка загрузки заявок: {e}")
    return requests