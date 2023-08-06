class EvaluateRequest:
    def __init__(self, flag_key, entity_id):
        self.flag_key = flag_key
        self.entity_id = entity_id

    def get_json(self):
        return {
            "flag_key": self.flag_key,
            "entity_id": self.entity_id
        }
