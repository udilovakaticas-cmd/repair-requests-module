import sqlite3
import os


def create_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        roleID INTEGER PRIMARY KEY AUTOINCREMENT,
        roleName TEXT NOT NULL
    )''')

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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        clientID INTEGER PRIMARY KEY AUTOINCREMENT,
        fio TEXT,
        phone TEXT
    )''')

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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
        commentID INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        masterID INTEGER,
        requestID INTEGER,
        FOREIGN KEY (masterID) REFERENCES Users(userID),
        FOREIGN KEY (requestID) REFERENCES Requests(requestID)
    )''')

    roles = [('Менеджер',), ('Мастер',), ('Оператор',)]
    cursor.executemany("INSERT OR IGNORE INTO Roles (roleName) VALUES (?)", roles)

    conn.commit()
    conn.close()
    print(f"База данных успешно создана по пути: {os.path.abspath(db_path)}")


if __name__ == "__main__":
    create_db()