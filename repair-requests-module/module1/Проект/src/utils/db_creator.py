import sqlite3
import os


def create_db():
    # Путь к файлу базы данных в корне проекта
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей (Foreign Keys)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Создание таблицы ролей (3НФ)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        roleID INTEGER PRIMARY KEY AUTOINCREMENT,
        roleName TEXT NOT NULL
    )''')

    # 2. Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        fio TEXT NOT NULL,
        phone TEXT,
        login TEXT UNIQUE,
        password TEXT,
        roleID INTEGER,
        FOREIGN KEY (roleID) REFERENCES Roles(roleID)
    )''')

    # 3. Создание таблицы клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        clientID INTEGER PRIMARY KEY AUTOINCREMENT,
        fio TEXT,
        phone TEXT
    )''')

    # 4. Создание таблицы заявок
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Requests (
        requestID INTEGER PRIMARY KEY AUTOINCREMENT,
        startDate TEXT,
        homeTechType TEXT,
        homeTechModel TEXT,
        problemDescription TEXT,
        requestStatus TEXT,
        completionDate TEXT,
        repairParts TEXT,
        masterID INTEGER,
        clientID INTEGER,
        FOREIGN KEY (masterID) REFERENCES Users(userID),
        FOREIGN KEY (clientID) REFERENCES Clients(clientID)
    )''')

    # 5. Создание таблицы комментариев
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
        commentID INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        masterID INTEGER,
        requestID INTEGER,
        FOREIGN KEY (masterID) REFERENCES Users(userID),
        FOREIGN KEY (requestID) REFERENCES Requests(requestID)
    )''')

    # Заполнение базовых ролей, если их нет
    roles = [('Менеджер',), ('Мастер',), ('Оператор',)]
    cursor.executemany("INSERT OR IGNORE INTO Roles (roleName) VALUES (?)", roles)

    conn.commit()
    conn.close()
    print(f"База данных успешно создана по пути: {os.path.abspath(db_path)}")


if __name__ == "__main__":
    create_db()