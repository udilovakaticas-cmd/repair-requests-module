class RepairRequest:
    def __init__(self, data):
        self.request_id = data['requestID']
        self.start_date = data['startDate']
        self.tech_type = data['homeTechType']
        self.tech_model = data['homeTechModel']
        self.problem = data['problemDescryption']
        self.status = data['requestStatus']
        self.master_id = data.get('masterID', '0')
        self.parts = data.get('repairParts', '')