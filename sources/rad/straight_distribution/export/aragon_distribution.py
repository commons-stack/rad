# this script returns a aragon-compatible dataframe for the exporter
import pandas as pd

# from ..distributions.straightDistribution import StraightDistribution


def run_export(_data, _config={}):
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

    final_token_allocations = pd.DataFrame(_data.distributionResults)

    final_alloc_aragon = final_token_allocations[["ID", "AMOUNT TO RECEIVE"]].copy()
    final_alloc_aragon["TOKEN SYMBOL"] = _data.tokenName

    # [TODO] Allow to send a link in the config dict that substitutes IDs for addresses
    #       Should come in handy for adding sourcecred

    final_alloc_aragon = final_alloc_aragon[
        final_alloc_aragon["ID"] != "missing user address"
    ]
    final_alloc_aragon = final_alloc_aragon.to_csv(sep=",", index=False, header=False)

    return final_alloc_aragon, ".csv"


def save_export(_name, _data, _config={}):

    export_file, export_extension = run_export(_data, _config)

    # filename = "export_" + _name + "_" + _config["type"] + ".csv"
    filename = _name + export_extension
    with open(filename, "w") as f:
        f.write(export_file)
