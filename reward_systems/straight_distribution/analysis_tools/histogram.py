from importlib.metadata import distribution
from ..straightDistribution import StraightDistribution
import plotly.express as px
import pandas as pd
import json


#change to markdown
header = "Histogram"
description = "Histo Histo Gram Gram"
author = "Nuggan"
Last_updated= "2022."
version=""

def run(straight_distribution_data):
    #print(type(straight_distribution_data))
    distribution = StraightDistribution.generate_from_dict(straight_distribution_data)
    res = distribution.distribution_results

    # initialize list of lists
    #data = [['tom', 10], ['nick', 15], ['juli', 14]]
 
    # Create the pandas DataFrame
    #res = pd.DataFrame(data, columns=['ID', 'AMOUNT TO RECEIVE'])
 
    # print dataframe.
    

    #print(type(res))
    #print(str(res))


    #distribution = pd.DataFrame()

    return res

def printGraph(straight_distribution_data):

    distribution = pd.DataFrame(run(straight_distribution_data))

    fig_freq = px.bar(distribution,  x=distribution.index, y="AMOUNT TO RECEIVE",labels={"AMOUNT TO RECEIVE": "Received","index": "Beneficiary"}, title="Rating Distribution", width=800, height=300)
    fig_freq.show()


#   #first we calculate the individual contributions of each praise giver
#   praise_by_giver = praise_distribution[['FROM USER ACCOUNT', 'AVG SCORE', 'PERCENTAGE', 'TOKEN TO RECEIVE']].copy().groupby(['FROM USER ACCOUNT']).agg('sum').reset_index()
#   praise_by_giver.rename(columns= {'TOKEN TO RECEIVE': 'TOKENS GAVE'}, inplace = True)
#   praise_by_giver.sort_values(by='TOKENS GAVE',inplace=True,ascending=False)

#   fig_praisegiver = px.bar(praise_by_giver, x="FROM USER ACCOUNT",y='TOKENS GAVE',title='Praise Giver Sorted by Total Score')
#   fig_praisegiver.show()