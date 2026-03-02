import sqlite3

def run_reports():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    print("=== ОТЧЕТ 1: КОЛИЧЕСТВО ЗАЯВОК ПО СТАТУСАМ ===")
    cursor.execute("SELECT requestStatus, COUNT(*) FROM Requests GROUP BY requestStatus")
    for row in cursor.fetchall():
        print(f"Статус: {row[0]} | Всего: {row[1]}")

    print("\n=== ОТЧЕТ 2: НАГРУЗКА НА МАСТЕРОВ ===")
    # Связываем Requests и Users, чтобы увидеть имена вместо ID
    query = """
    SELECT u.fio, COUNT(r.requestID) 
    FROM Users u
    JOIN Requests r ON u.userID = r.masterID 
    GROUP BY u.fio
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"Мастер: {row[0]} | Заявок в работе: {row[1]}")

    conn.close()

if __name__ == "__main__":
    run_reports()