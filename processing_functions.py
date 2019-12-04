"""Functions made to combine spreadsheets to a clear, organised, standard format."""

import pandas as pd


# Functions that combine paired and individual bet spreadsheets 

def remove_wanted_columns(spreadsheet):
    """Removes unwanted columns from a preprocessed individual bets spreadsheet."""
    
    spreadsheet.drop(['BookieID', 'BetOutcomeID', 'BettingTypeID', 'ItemID'], 
                     axis=1, inplace=True)
    
    return spreadsheet


def tidy_profit_id(spreadsheet):
    """Renames preprocessed individual bets spreadsheets' profitid to ProfitID.
       This allowed paired and individual bets to be merged on ProfitID."""
    
    spreadsheet.rename(columns={'profitid':'ProfitID'}, inplace=True)
    
    return spreadsheet


def merge_on_profit_id(individual_spreadsheet, paired_spreadsheet):
    """Combines paired and individual spreadsheets to make a new spreadsheet.
    
       It does this by taking columns exclusive to paired bet spreadsheets and 
       merges to individual bets spreadsheets based on Profit ID."""
    
    for column in ['sport', 'Event', 'EventTime', 'datecreated ', 'BetType', 'Note']:
        partially_merged = pd.merge(individual_spreadsheet, 
                                    paired_spreadsheet.loc[:,['ProfitID',column]], 
                                    on='ProfitID')
        individual_spreadsheet = partially_merged
        
    return individual_spreadsheet


# Functions that better organise and tidy up the newly combined spreadsheet 

def rename_colums(spreadsheet):
    """Renames columns on newly combined spreadsheet."""
    
    spreadsheet.columns = ['Profit ID', 'Bookie', 'Bet Result', 'Type', 
                               'Outcome', 'Stake','Odds', 'Fee (%)', 'Liability', 
                               'Return', 'Potential Profit', 'Sport', 'Event', 
                               'Event Time', 'Date Created', 'Bet Type', 'Note']
    
    return spreadsheet


def reorder_columns(spreadsheet):
    """Reorders columns on newly combined spreadsheet."""
    
    columns_reordered = ['Date Created', 'Sport', 'Event', 'Event Time', 'Bookie',
                         'Bet Type','Type', 'Outcome', 'Stake', 'Odds', 'Fee (%)', 
                         'Liability', 'Return','Potential Profit', 'Bet Result',
                         'Note', 'Profit ID']
    
    spreadsheet = spreadsheet.loc[:, columns_reordered]
    
    return spreadsheet


def rename_type_normal(spreadsheet):
    """Renames to Bet Type 'Normal' to 'Qualifying' to better represent what the 
       bet does (qualify for free bet)."""
    
    spreadsheet.loc[:,'Bet Type'].replace('Normal', 'Qualifying', inplace=True)
    
    return spreadsheet


def fill_note_NaN(spreadsheet):
    """Replace NaNs in notes with blank space."""
    
    spreadsheet.loc[:, 'Note'].fillna(' ', inplace=True)
    
    return spreadsheet


def win_lose_indices(winning_indices_list):
    """Input a list of indices of winning bets.
       Returns a tuple (list 1, list2, list3).
    
       list 1: indices of winning bets
       list 2: indices of subsequent losing bets
       list 3: indices of winning and losing bets
       
       If the smallest winning index is odd, then its paired bet (the preceeding index), 
       will be that of a losing bet and must be included in the losing index list.
       
       If the largest winning index is even, then its paired bet (the proceeding index), 
       will be that of a losing bet and must be included in the losing index list."""
    
    if min(winning_indices_list) % 2 == 0:
        range_min = min(winning_indices_list)
    else:
        range_min = min(winning_indices_list) - 1
    
    if max(winning_indices_list) % 2 == 0:
        range_max = max(winning_indices_list) + 2
    else:
        range_max = max(winning_indices_list) + 1
    
    bets_to_be_updated = range(range_min, range_max)
    losing_indices_list = list(set(bets_to_be_updated) - set(winning_indices_list))
    
    return (winning_indices_list, losing_indices_list, list(bets_to_be_updated))


def update_bet_results(spreadsheet, winning_indices_list):
    """Updates the spreadsheet with which bets won and lost."""
    
    win_lose_tuple = win_lose_indices(winning_indices_list)

    spreadsheet.loc[win_lose_tuple[0], 'Bet Result'] = "Win"
    spreadsheet.loc[win_lose_tuple[1], "Bet Result"] = "Lose"
    
    return spreadsheet
