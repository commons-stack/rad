class RewardSystem:
    def __init__(self, _name) -> None:
        self.name = _name

    @classmethod
    def generate_from_params(cls, _params):
        raise NotImplementedError("Please Implement this method")
