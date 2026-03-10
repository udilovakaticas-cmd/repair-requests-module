import csv
import os
from tkinter import messagebox

def get_project_root():
    current_path = os.path.dirname(os.path.abspath(__file__))
    # Пробуем подняться на 2 уровня (из utils в src, затем в корень)
    root = os.path.abspath(os.path.join(current_path, '..', '..'))
    if not os.path.exists(os.path.join(root, 'data')):
        root = os.path.abspath(os.path.join(current_path, '..'))
    return root

def load_users(project_root):
    user_file = os.path.join(project_root, 'data', 'inputDataUsers.csv')
    if not os.path.exists(user_file):
        os.makedirs(os.path.dirname(user_file), exist_ok=True)
        with open(user_file, mode='w', encoding='utf-8', newline='') as f:
            f.write("userID;fio;phone;login;password;type\n")
            f.write("10;Иван Тестов;89991112233;client;123;Заказчик\n")
    users = []
    try:
        with open(user_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                users.append(row)
    except Exception as e:
        print(f"Ошибка чтения пользователей: {e}")
    return users

def load_all_data(project_root):
    from models.request import RepairRequest
    req_file = os.path.join(project_root, 'data', 'inputDataRequests.csv')
    if not os.path.exists(req_file):
        os.makedirs(os.path.dirname(req_file), exist_ok=True)
        with open(req_file, mode='w', encoding='utf-8', newline='') as f:
            f.write("requestID;startDate;homeTechType;homeTechModel;problemDescryption;requestStatus;completionDate;repairParts;masterID;clientID\n")
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
                    'repairParts': getattr(req, 'parts', ''),
                    'masterID': getattr(req, 'master_id', '0'),
                    'clientID': getattr(req, 'client_id', '1')
                })
        return True
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось записать данные: {e}")
        return False

def save_comment(request_id, message, master_id):
    """Сохраняет комментарий мастера в inputDataComments.csv"""
    root = get_project_root()
    comment_file = os.path.join(root, 'data', 'inputDataComments.csv')
    count = 1
    if os.path.exists(comment_file):
        try:
            with open(comment_file, mode='r', encoding='utf-8') as f:
                count = sum(1 for _ in f)
        except: count = 1
    try:
        file_exists = os.path.isfile(comment_file)
        with open(comment_file, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            if not file_exists:
                writer.writerow(['commentID', 'message', 'masterID', 'requestID'])
            writer.writerow([count, message, master_id, request_id])
        return True
    except Exception as e:
        print(f"Ошибка записи комментария: {e}")
        return False

def show_feedback_qr():
    """Генерирует QR-код и выводит его в красивом окне приложения"""
    import qrcode
    from PIL import ImageTk, Image
    import customtkinter as ctk

    # Создаем окно
    qr_window = ctk.CTkToplevel()
    qr_window.title("Оценка качества")
    qr_window.geometry("350x450")
    qr_window.attributes("-topmost", True)

    # Текст над кодом
    ctk.CTkLabel(qr_window, text="Оцените нашу работу!", font=("Arial", 18, "bold")).pack(pady=20)

    # Генерация QR-кода (ссылка на форму или сайт)
    link = "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform?usp=sf_link" # Твоя ссылка
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(link)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white")
    # Превращаем в формат, который понимает Tkinter
    img_tk = ImageTk.PhotoImage(img_qr)

    # Отображаем картинку
    qr_label = ctk.CTkLabel(qr_window, image=img_tk, text="")
    qr_label.image = img_tk  # Важно сохранить ссылку, чтобы картинка не исчезла
    qr_label.pack(pady=10)

    ctk.CTkLabel(qr_window, text="Отсканируйте камерой телефона", font=("Arial", 12)).pack(pady=10)

    # Кнопка закрытия
    ctk.CTkButton(qr_window, text="Закрыть", command=qr_window.destroy).pack(pady=20)