class EvaluateRequest:
    def __init__(self, flag_key, user_id):
        self.flag_key = flag_key
        self.user_id = user_id

    def get_json(self):
        return {
            "flag_key": self.flag_key,
            "entity_id": self.user_id
        }
