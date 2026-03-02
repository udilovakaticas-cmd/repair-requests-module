class AuthService:

    def __init__(self):
        # Примеры пользователей
        self.users = [
            {"login": "admin", "password": "1234", "role": "Администратор"},
            {"login": "user", "password": "1234", "role": "Пользователь"},
            {"login": "operator", "password": "1234", "role": "Оператор"},
            {"login": "master", "password": "1234", "role": "Мастер"}
        ]

    def authenticate(self, login, password):
        for user in self.users:
            if user["login"] == login and user["password"] == password:
                return user
        return None