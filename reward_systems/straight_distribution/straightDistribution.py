# distribution where everybody gets the same (eg. rewardboard)
import pandas as pd

from src.rewardSystem import RewardSystem


class StraightDistribution(RewardSystem):

    def __init__(self, _beneficiaries, _distAmount, _tokenName, _tokenAddress) -> None:
        super().__init__("praise")
        self.beneficiaries = _beneficiaries
        self.totalDistAmount = _distAmount
        self.tokenName = _tokenName
        self.tokenAddress = _tokenAddress
        self.distributionResults = pd.DataFrame()

        self.do_distribution()

    @classmethod
    def generate_from_params(cls, _params):
        beneficiaries = pd.read_csv(_params["input_files"]["beneficiary_list"])
        distAmount = _params["distribution_amount"]
        tokenName = _params["payout_token"]["token_name"]
        tokenAddress = _params["payout_token"]["token_address"]

        return cls(_beneficiaries=beneficiaries, _distAmount=distAmount, _tokenName=tokenName, _tokenAddress=tokenAddress)

    def do_distribution(self) -> None:

        self.distributionResults = pd.DataFrame(self.beneficiaries)
        self.distributionResults['AMOUNT TO RECEIVE'] = self.totalDistAmount / \
            len(self.distributionResults.index)

    def get_distribution_results(this) -> pd.DataFrame:
        return this.distributionResults
