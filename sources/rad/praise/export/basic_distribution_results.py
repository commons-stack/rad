import pandas as pd
from ..praiseObj import Praise


def run_export(_filename, _data, _config={}):
    """
    Creates a CSV file of the distribution.

        Args:
            _data: the necessary data to generate it
            _config:(Optional) dict with extra configuration data, if necessary.
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves it
    """

    _filename += ".csv"

    final_token_allocations = pd.DataFrame(_data.distributionResults)
    final_allocation_csv = final_token_allocations.to_csv(sep=",", index=False)

    with open(_filename, "w") as f:
        f.write(final_allocation_csv)

    return
