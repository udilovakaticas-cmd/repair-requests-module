class RepairRequest:

    def __init__(
        self,
        request_id,
        date_added,
        device_type,
        model,
        problem_description,
        client_name,
        phone,
        status="новая заявка",
        master=None,
        date_completed=None
    ):
        self.request_id = request_id
        self.date_added = date_added
        self.device_type = device_type
        self.model = model
        self.problem_description = problem_description
        self.client_name = client_name
        self.phone = phone
        self.status = status
        self.master = master
        self.date_completed = date_completed