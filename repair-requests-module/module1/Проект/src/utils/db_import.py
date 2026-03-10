import sqlite3
import csv
import os


def import_csv_to_db():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    db_path = os.path.join(root, 'database.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    users_path = os.path.join(root, 'data', 'inputDataUsers.csv')
    if os.path.exists(users_path):
        with open(users_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                role_map = {'Менеджер': 1, 'Мастер': 2, 'Оператор': 3}
                role_id = role_map.get(row['type'], 2)

                cursor.execute("""
                    INSERT OR IGNORE INTO Users (userID, fio, phone, login, password, roleID)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (row['userID'], row['fio'], row['phone'], row['login'], row['password'], role_id))

    req_path = os.path.join(root, 'data', 'inputDataRequests.csv')
    if os.path.exists(req_path):
        with open(req_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                cursor.execute("""
                    INSERT OR IGNORE INTO Requests 
                    (requestID, startDate, homeTechType, homeTechModel, problemDescription, requestStatus, masterID, clientID)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (row['requestID'], row['startDate'], row['homeTechType'], row['homeTechModel'],
                      row['problemDescryption'], row['requestStatus'], row['masterID'], row['clientID']))

    conn.commit()
    conn.close()
    print("Данные успешно импортированы из CSV в базу данных!")


if __name__ == "__main__":
    import_csv_to_db()