def validate_request_data(data):
    if not data.get('problemDescryption'):
        return False, "Описание проблемы не может быть пустым"
    return True, ""