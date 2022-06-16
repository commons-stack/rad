# distribution where everybody gets the same (eg. rewardboard)
import pandas as pd

from src.rewardSystem import RewardSystem


class StraightDistribution(RewardSystem):

    def __init__(self, _benficiaries, _distAmount, _tokenName, _tokenAddress) -> None:
        super().__init__("praise")
        self.beneficiaries = _benficiaries
        self.totalDistAmount = _distAmount
        self.tokenName = _tokenName
        self.tokenAddress = _tokenAddress
        self.distributionResults = pd.DataFrame()

        self.do_distribution()

    def do_distribution(self) -> None:

        self.distributionResults = pd.DataFrame(self.beneficiaries)
        self.distributionResults['AMOUNT TO RECEIVE'] = self.totalDistAmount / \
            len(self.distributionResults.index)
