class AuthService:

    def __init__(self):
        self.users = [
            {"login": "admin", "password": "1234", "role": "admin"},
            {"login": "operator", "password": "1111", "role": "operator"},
            {"login": "master", "password": "2222", "role": "master"}
        ]

    def authenticate(self, login, password):
        for user in self.users:
            if user["login"] == login and user["password"] == password:
                return user
        return None