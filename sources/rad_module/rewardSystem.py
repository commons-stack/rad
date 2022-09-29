class RewardSystem(object):
    def __init__(self, _name, _type) -> None:
        self.name = _name
        self.type = _type

    @classmethod
    def generate_from_params(cls, _params):
        raise NotImplementedError("Please Implement this method")

    @classmethod
    def import_from_dict(cls, self, _dict):
        self.name = _dict["name"]
        self.type = _dict["type"]

    @classmethod
    def export_to_dict(cls, self):
        exp_dict = {}

        exp_dict["name"] = self.name
        exp_dict["type"] = self.type

        return exp_dict
