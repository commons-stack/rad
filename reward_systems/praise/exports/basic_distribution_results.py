import pandas as pd
from ..praise import Praise


def run_export(_data, _config={}):
    """
    Creates a CSV file of the distribution.

        Args:
            _data: the necessary data to generate it
            _config:(Optional) dict with extra configuration data, if necessary.
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """

    final_token_allocations = pd.DataFrame(_data.distributionResults)
    final_allocation_csv = final_token_allocations.to_csv(sep=",", index=False)

    return final_allocation_csv, ".csv"
