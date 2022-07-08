# this script returns a aragon-compatible dataframe for the exporter
import pandas as pd
from ..straightDistribution import StraightDistribution


def run_export(_data, _config={}):
    # distribution = StraightDistribution(_data)

    final_token_allocations = pd.DataFrame(_data.distribution_results)

    final_alloc_aragon = final_token_allocations[["ID", "AMOUNT TO RECEIVE"]].copy()
    final_alloc_aragon["TOKEN SYMBOL"] = _data.tokenName
    final_alloc_aragon = final_alloc_aragon[
        final_alloc_aragon["ID"] != "missing user address"
    ]
    final_alloc_aragon = final_alloc_aragon.to_csv(sep=",", index=False, header=False)

    return final_alloc_aragon
