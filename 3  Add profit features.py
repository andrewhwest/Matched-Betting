"""Add profit to spreadsheet and keep track of money across various bookmaker accounts"""

import pandas as pd
from balance_functions import *


bet_spreadsheet = pd.read_csv('Bet Spreadsheet with missing bets added.csv')

# Calculate profit from bet result
win_lose_boolean = (bet_spreadsheet['Bet Result'] == 'Win')
bet_profit = bet_spreadsheet['Potential Profit'] * win_lose_boolean

# Add profit as a column 
column_after_Bet_Result = bet_spreadsheet.columns.get_loc('Bet Result') + 1
bet_spreadsheet.insert(column_after_Bet_Result, 'Profit', bet_profit)

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

# Remove minus from -0.00 in profit
bet_spreadsheet.iloc[:, -3] = bet_spreadsheet.iloc[:, -3].apply(lambda x : abs(x) 
                                                                if (x == -0.00) else x)
# Add Running Profit as a column
column_after_Profit = column_after_Bet_Result + 1 
bet_spreadsheet.insert(column_after_Profit, 'Running Profit', bet_spreadsheet['Profit'].cumsum())

# Show balances for each bookmaker
bookie_balances(bet_spreadsheet)

# Save changes
bet_spreadsheet.to_csv('Bet Spreadsheet with profit features.csv', index=False)
