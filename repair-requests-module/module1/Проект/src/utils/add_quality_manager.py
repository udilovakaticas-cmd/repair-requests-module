import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')

if not os.path.exists(db_path):
    print(f"Ошибка: База данных не найдена по пути {os.path.abspath(db_path)}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT OR IGNORE INTO Roles (roleName) VALUES ('Менеджер по качеству')")


        cursor.execute("""
            INSERT OR IGNORE INTO Users (fio, phone, login, password, roleID) 
            VALUES ('Смирнова А.А.', '89001112233', 'quality', '12345', 4)
        """)

        conn.commit()
        print("Менеджер по качеству успешно добавлен!")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        conn.close()