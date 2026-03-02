def validate_request_data(data):
    """Простейшая проверка: поля не должны быть пустыми"""
    if not data.get('problemDescryption'):
        return False, "Описание проблемы не может быть пустым"
    return True, ""