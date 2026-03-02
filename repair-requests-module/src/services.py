from models import RepairRequest
from datetime import datetime


class RequestService:

    def __init__(self):
        self.requests = []

    def add_request(
        self,
        device_type,
        model,
        problem_description,
        client_name,
        phone
    ):
        request_id = len(self.requests) + 1
        date_added = datetime.now()

        new_request = RepairRequest(
            request_id,
            date_added,
            device_type,
            model,
            problem_description,
            client_name,
            phone
        )

        self.requests.append(new_request)

        return new_request

    def get_all_requests(self):
        return self.requests