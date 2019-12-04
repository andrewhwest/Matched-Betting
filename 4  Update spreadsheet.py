"""Reads new updated paired and individual bet files to extract new bets and then combine them with the old bets.
New bets are added as unsettled and then results and profit are updated when the sporting events finish."""

import pandas as pd 
from processing_functions import *
from balance_functions import *
from updating_functions import *


## Read old spreadsheet

old_bet_spreadsheet = pd.read_csv('Bet Spreadsheet with profit features.csv')


## Separate new individual bets from old

# Updated files contain old and new bets
updated_individual_bets = pd.read_csv('Updated individual bets.csv')

# Remove a rare bet that was causing problems
updated_individual_bets = remove_individual_bet(updated_individual_bets)

# Spreadsheet of new individual bets
new_individual_bets = new_individual_spreadsheet(old_bet_spreadsheet, updated_individual_bets)


## Separate new paired bets from old

# Updated files contain old and new bets
updated_paired_bets = pd.read_csv('Updated paired bets.csv')

# Remove a rare bet that was causing problems
updated_paired_bets = remove_paired_bet(updated_paired_bets)

# Spreadsheet of new paired bets
new_paired_bets = new_paired_spreadsheet(new_individual_bets, updated_paired_bets)


## Combine new paired and individual bets

new_individual_bets = remove_wanted_columns(new_individual_bets)
new_individual_bets = tidy_profit_id(new_individual_bets)
new_bets = merge_on_profit_id(new_individual_bets, new_paired_bets)
new_bets = rename_colums(new_bets)
new_bets = reorder_columns(new_bets)
new_bets = rename_type_normal(new_bets)
new_bets = fill_note_NaN(new_bets)
new_bets = fill_bet_result_NaN(new_bets)
new_bets = add_profit_column(new_bets)
new_bets = running_profit(new_bets)


## Combine old and new unsettled bets

# Concat to make new spreadsheet with unsettled bets
bet_spreadsheet = pd.concat([old_bet_spreadsheet, new_bets], ignore_index=True)

# Save new spreadsheet
bet_spreadsheet.to_csv('Bet Spreadsheet with new unsettled bets.csv', index=False)


## Settle bets

# Settle bet results
win_list = [21, 22, 25, 27, 28, 31, 33]
bet_spreadsheet = update_bet_results(bet_spreadsheet, win_list)

# Calculate profit for settled bets
newly_settled_bets_list = win_lose_indices(win_list)[2]
newly_settled_bets = bet_spreadsheet.loc[newly_settled_bets_list]
bet_spreadsheet.loc[newly_settled_bets_list] = calculate_profit(newly_settled_bets)

# Check bookie balances for settled bets
bookie_balances(bet_spreadsheet.loc[newly_settled_bets_list])

# Recalculate running profit for whole spreadsheet
bet_spreadsheet = recalculate_running_profit(bet_spreadsheet)

# Save completely update to date spreadsheet
bet_spreadsheet.to_csv('Bet Spreadsheet with new settled bets.csv', index=False)
