"""Combines two spreadsheets to make a new master spreadsheet.

   A website I use for matched betting provides two speadsheets.
   The first one contains information for each individual bet placed.
   The second gives a summary for each pair of bets that were placed on the same
   sporting event.
   
   This script combines and organises information from both.
"""

import pandas as pd
from processing_functions import *


# Read csv files
paired_bets_file = 'file path.../Paired\ Bets.csv'
paired_bets_file = paired_bets_file.replace("\\", "")
paired_bets = pd.read_csv(paired_bets_file)

individual_bets_file = 'file path.../Individual\ Bets.csv'
individual_bets_file = individual_bets_file.replace("\\", "")
individual_bets = pd.read_csv(individual_bets_file)

# Combine paired and individual spreadsheets

individual_bets = remove_wanted_columns(individual_bets)

individual_bets = tidy_profit_id(individual_bets)

bet_spreadsheet = merge_on_profit_id(individual_bets, paired_bets)
  
# Better organise and tidy up the newly combined spreadsheet.

bet_spreadsheet = rename_colums(bet_spreadsheet)

bet_spreadsheet = reorder_columns(bet_spreadsheet)

bet_spreadsheet = rename_type_normal(bet_spreadsheet)

bet_spreadsheet = fill_note_NaN(bet_spreadsheet)

# Update bet results

bet_spreadsheet = update_bet_results(bet_spreadsheet, [0,2,5,6,9,10,13,15])

# Save new spreadsheet
bet_spreadsheet.to_csv('Bet Spreadsheet.csv', index=False)


