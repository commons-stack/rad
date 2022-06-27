import plotly.express as px

header = "Histogram"
description = "Histo Histo Gram Gram"
author = "Nuggan"
Last_updated= "2022."
version=""

def run(straight_distribution_data):

    distribution = StraightDistribution(straight_distribution_data).get_distribution_results()

    return distribution

def print(self, straight_distribution_data):

    distribution = self.run(straight_distribution_data)

    fig_freq = px.bar(distribution,  x="index", y="AMOUNT TO RECEIVE",labels={"AMOUNT TO RECEIVE": "Received","index": "Beneficiary"}, title="Rating Distribution", width=800, height=300)
    fig_freq.show()


#   #first we calculate the individual contributions of each praise giver
#   praise_by_giver = praise_distribution[['FROM USER ACCOUNT', 'AVG SCORE', 'PERCENTAGE', 'TOKEN TO RECEIVE']].copy().groupby(['FROM USER ACCOUNT']).agg('sum').reset_index()
#   praise_by_giver.rename(columns= {'TOKEN TO RECEIVE': 'TOKENS GAVE'}, inplace = True)
#   praise_by_giver.sort_values(by='TOKENS GAVE',inplace=True,ascending=False)

#   fig_praisegiver = px.bar(praise_by_giver, x="FROM USER ACCOUNT",y='TOKENS GAVE',title='Praise Giver Sorted by Total Score')
#   fig_praisegiver.show()