"""Add profit to spreadsheet and keep track of money across various bookmaker accounts"""

import pandas as pd
from balance_functions import *


bet_spreadsheet = pd.read_csv('Bet Spreadsheet with missing bets added.csv')

# Add profit
bet_spreadsheet = add_profit_column(bet_spreadsheet)
bet_spreadsheet = calculate_profit(bet_spreadsheet)

# Tidy up note on rows 12 and 13
bet_spreadsheet.loc[[12,13], 'Note'] = '''Liability changed last minute to 118.01, 
                                        stake to 21.07, back bet won, profit=150-118.01'''

# Update profit based on note 
bet_spreadsheet.loc[[12,13], 'Profit'] = 31.99

# £10 of losses was refunded by smarkets as part of a promotion
bet_spreadsheet.loc[[2,3], 'Note'] = '2.67 of losses from exchange refunded'
bet_spreadsheet.loc[2, 'Profit'] = 2.57
bet_spreadsheet.loc[[6,7], 'Note'] = '7.33 of losses from exchange refunded'
bet_spreadsheet.loc[6, 'Profit'] = 7

# Add running profit
bet_spreadsheet = remove_negative_zeros(bet_spreadshet)
bet_spreadsheet = running_profit(bet_spreadsheet)

# Show balances for each bookmaker
bookie_balances(bet_spreadsheet)

# Save changes
bet_spreadsheet.to_csv('Bet Spreadsheet with profit features.csv', index=False)
