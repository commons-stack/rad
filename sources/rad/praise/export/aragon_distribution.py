# this script returns a aragon-compatible dataframe for the exporter
import pandas as pd

# from ..distributions.standard_praise import PraiseDistribution


def run_export(_filename, _data, _config={}):
    """
    Creates an Aragon-Transactions-friendly distribution CSV.

        Args:
            _data: the necessary data to generate it
            _config:(Optional) dict with extra configuration data. Allows to link to a file which maps User IDs to addresses to subsititute in the rewards object
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """
    _filename += ".csv"

    final_token_allocations = pd.DataFrame(_data.distributionResults)

    final_alloc_aragon = final_token_allocations[
        ["USER ADDRESS", "TOTAL TO RECEIVE"]
    ].copy()
    final_alloc_aragon["TOKEN SYMBOL"] = _data.tokenName

    # [TODO] Allow to send a link in the config dict that substitutes IDs for addresses
    #       Should come in handy for adding sourcecred

    final_alloc_aragon = final_alloc_aragon[
        final_alloc_aragon["USER ADDRESS"] != "missing user address"
    ]
    final_alloc_aragon = final_alloc_aragon.to_csv(sep=",", index=False, header=False)

    with open(_filename, "w") as f:
        f.write(final_alloc_aragon)

    return
