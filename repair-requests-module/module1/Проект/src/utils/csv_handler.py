import csv
import os
from tkinter import messagebox

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

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


def save_requests(requests_list):
    root = get_project_root()
    req_file = os.path.join(root, 'data', 'inputDataRequests.csv')

    try:
        with open(req_file, mode='w', encoding='utf-8', newline='') as f:
            fieldnames = [
                'requestID', 'startDate', 'homeTechType', 'homeTechModel',
                'problemDescryption', 'requestStatus', 'completionDate',
                'repairParts', 'masterID', 'clientID'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

            for req in requests_list:
                writer.writerow({
                    'requestID': req.request_id,
                    'startDate': req.start_date,
                    'homeTechType': req.tech_type,
                    'homeTechModel': req.tech_model,
                    'problemDescryption': req.problem,
                    'requestStatus': req.status,
                    'completionDate': getattr(req, 'completion_date', ''),
                    'repairParts': req.parts,
                    'masterID': req.master_id,
                    'clientID': getattr(req, 'client_id', '1')  # Заглушка по умолчанию
                })
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось записать данные: {e}")


def save_comment(request_id, message, master_id):
    root = get_project_root()
    comment_file = os.path.join(root, 'data', 'inputDataComments.csv')

    try:
        with open(comment_file, mode='r', encoding='utf-8') as f:
            count = sum(1 for line in f)
    except FileNotFoundError:
        count = 1

    try:
        with open(comment_file, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([count, message, master_id, request_id])
    except Exception as e:
        print(f"Ошибка записи комментария: {e}")