class User:
    def __init__(self, data):
        self.user_id = data.get('userID')
        self.fio = data.get('fio')
        self.phone = data.get('phone')
        self.login = data.get('login')
        self.password = data.get('password')
        self.type = data.get('type')