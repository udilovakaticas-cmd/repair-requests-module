from datetime import datetime

class Request:
    _id_counter = 1

    def __init__(self, device, model, problem, client, phone, time_to_complete):
        self.request_id = Request._id_counter
        Request._id_counter += 1

        self.date_added = datetime.now()
        self.device_type = device
        self.model = model
        self.problem_description = problem
        self.client_name = client
        self.phone = phone
        self.time_to_complete = time_to_complete
        self.status = "новая заявка"


class RequestService:

    def __init__(self):
        self.requests = []

    def add_request(self, device, model, problem, client, phone, time_to_complete):
        req = Request(device, model, problem, client, phone, time_to_complete)
        self.requests.append(req)

    def get_all_requests(self):
        return self.requests