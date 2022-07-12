import pandas as pd
from ..praise import Praise


def run_export(_data, _config={}):
    """
    Creates a CSV file of the full praise dataset.

        Args:
            _data: the necessary data to generate it
            _config:(Optional) dict with extra configuration data, if necessary.
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """

    extended_praise_table = pd.DataFrame(_data.dataTable)
    final_allocation_csv = extended_praise_table.to_csv(sep=",", index=False)

    return final_allocation_csv
