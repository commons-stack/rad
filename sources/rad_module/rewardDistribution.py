class RewardDistribution:
    def __init__(self, _name, _type) -> None:
        self.name = _name
        self.type = _type

    @classmethod
    def generate_from_params(cls, _params):
        raise NotImplementedError("Please Implement this method")
