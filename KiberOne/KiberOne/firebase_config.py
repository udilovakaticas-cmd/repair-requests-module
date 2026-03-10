import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Список пользователей для добавления
users = [
    {
        "user_id": "admin_1",
        "name": "Екатерина",
        "surname": "Удилова",
        "role": "admin",
        "age": 21,
        "pin": "",
        "avatar": "",
        "progress_level": 0,
        "direction": "",
        "test_results": {}
    },
    {
        "user_id": "teacher_1",
        "name": "Кристина",
        "surname": "",
        "role": "teacher",
        "age": 24,
        "pin": "",
        "avatar": "",
        "progress_level": 0,
        "direction": "",
        "test_results": {}
    },
    {
        "user_id": "student_1",
        "name": "Кирилл",
        "surname": "Хазиев",
        "role": "student",
        "age": 12,
        "pin": "1234",
        "avatar": "cat_coder",
        "progress_level": 0,
        "direction": "programming",
        "test_results": {}
    },
    {
        "user_id": "student_2",
        "name": "Алиса",
        "surname": "Сахарова",
        "role": "student",
        "age": 9,
        "pin": "5678",
        "avatar": "fox_designer",
        "progress_level": 0,
        "direction": "design",
        "test_results": {}
    },
    {
        "user_id": "student_3",
        "name": "Иван",
        "surname": "Николаев",
        "role": "student",
        "age": 13,
        "pin": "9012",
        "avatar": "owl_gamer",
        "progress_level": 0,
        "direction": "3d",
        "test_results": {}
    }
]

# Добавляем пользователей в коллекцию 'users'
for user in users:
    db.collection("users").document(user["user_id"]).set(user)
    print(f"Добавлен пользователь: {user['name']} {user['surname']}")

# Список тестов
tests = [
    {
        "test_id": "test_1",
        "title": "Основы ПК",
        "description": "Проверка базовых навыков работы с компьютером",
        "age_range": "6-8",
        "direction": "computer_literacy",
        "questions": [
            {"q": "Что такое мышь?", "options": ["Устройство ввода", "Программа", "Кнопка"], "answer": "Устройство ввода"},
            {"q": "Как открыть папку?", "options": ["Кликнуть дважды", "Написать в блокноте", "Выключить"], "answer": "Кликнуть дважды"}
        ]
    },
    {
        "test_id": "test_2",
        "title": "Программирование Scratch",
        "description": "Проверка базовых навыков программирования в Scratch",
        "age_range": "6-8",
        "direction": "programming",
        "questions": [
            {"q": "Что делает блок 'двигаться на 10 шагов'?", "options": ["Перемещает спрайт", "Меняет фон", "Добавляет звук"], "answer": "Перемещает спрайт"},
            {"q": "Как запустить скрипт?", "options": ["Клик по зелёному флагу", "Нажать ESC", "Закрыть проект"], "answer": "Клик по зелёному флагу"}
        ]
    }
]

# Добавляем тесты в коллекцию 'tests'
for test in tests:
    db.collection("tests").document(test["test_id"]).set(test)
    print(f"Добавлен тест: {test['title']}")

# Список аватаров
avatars = [
  {"avatar_id": "fox", "name": "Фокси", "image_url": "url_to_fox_image"},
  {"avatar_id": "owl", "name": "Сова", "image_url": "url_to_owl_image"},
  {"avatar_id": "cat", "name": "Котик", "image_url": "url_to_cat_image"},
  {"avatar_id": "dog", "name": "Пёсик", "image_url": "url_to_dog_image"}
]

# Добавляем аватары в коллекцию 'avatars'
for avatar in avatars:
    db.collection("avatars").document(avatar["avatar_id"]).set(avatar)
    print(f"Добавлен аватар: {avatar['name']}")
