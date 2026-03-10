class RepairRequest:
    def __init__(self, data):
        self.request_id = data.get('requestID')
        self.start_date = data.get('startDate')
        self.tech_type = data.get('homeTechType')
        self.tech_model = data.get('homeTechModel')
        self.problem = data.get('problemDescryption')
        self.status = data.get('requestStatus')
        self.master_id = data.get('masterID', '0')
        self.client_id = data.get('clientID', '0')
        self.completion_date = data.get('completionDate', '')
        self.parts = data.get('repairParts', '')