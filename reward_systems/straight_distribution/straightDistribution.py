# distribution where everybody gets the same (eg. rewardboard)
from importlib.metadata import distribution
import pandas as pd

from src.rewardSystem import RewardSystem


class StraightDistribution(RewardSystem):
    def __init__(
        self,
        _beneficiaries,
        _distAmount,
        _tokenName,
        _tokenAddress,
        _distributionResults={},
    ):
        super().__init__("praise")
        self.beneficiaries = _beneficiaries
        self.totalDistAmount = int(_distAmount)
        self.tokenName = _tokenName
        self.tokenAddress = _tokenAddress
        self.distributionResults = _distributionResults

        if _distributionResults == {}:
            self.do_distribution()

    def __str__(self):
        return (
            "From str method of StrightDistr: totalDistAmount is % s, tokenName is % s, results are % s"
            % (self.totalDistAmount, self.tokenName, str(self.distribution_results))
        )

    @classmethod
    def generate_from_params(cls, _params):
        beneficiaries_input = pd.read_csv(_params["input_files"]["beneficiary_list"])
        # lets pipe this through pandas to be sure we don't run into issues
        beneficiaries = pd.DataFrame.to_dict(beneficiaries_input)
        distAmount = _params["distribution_amount"]
        tokenName = _params["payout_token"]["token_name"]
        tokenAddress = _params["payout_token"]["token_address"]

        return cls(
            _beneficiaries=beneficiaries,
            _distAmount=distAmount,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
        )

    @classmethod
    def generate_from_dict(cls, _dict):

        beneficiaries = _dict["beneficiaries"]
        distAmount = _dict["totalDistAmount"]
        tokenName = _dict["tokenName"]
        tokenAddress = _dict["tokenAddress"]
        distributionResults = _dict["distributionResults"]

        return cls(
            _beneficiaries=beneficiaries,
            _distAmount=distAmount,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
            _distributionResults=distributionResults,
        )

    def do_distribution(self) -> None:

        dist_results = pd.DataFrame.from_dict(self.beneficiaries)
        dist_results["AMOUNT TO RECEIVE"] = self.totalDistAmount / len(
            dist_results.index
        )
        self.distribution_results = pd.DataFrame.to_dict(dist_results)

    def get_distribution_results(self):
        # [TODO]broken. fix
        return pd.DataFrame.from_dict(self.distributionResults)
