"""Functions used to update an old spreadsheet with new bets."""

import pandas as pd


## Separate new individual bets from old

def remove_individual_bet(updated_individual_spreadsheet):
    """Removes a rare bet that was causing lots of problems"""
    
    updated_individual_spreadsheet.drop([22], inplace=True)
    
    return updated_individual_spreadsheet


def new_individual_spreadsheet(old_spreadsheet, updated_individual_spreadsheet):
    """Returns a spreadsheet of new individual bets that need to be added 
       to the old spreadsheet."""

    first_new_bet = len(old_spreadsheet) - 4
    # 4 accounts for the missing bets that arent't in individual bet files
    
    new_individual_bets = updated_individual_spreadsheet.iloc[first_new_bet:, ]
    
    return new_individual_bets

## Separate new paired bets from old

def remove_paired_bet(updated_paired_spreadsheet):
    """Removes a rare bet that was causing lots of problems"""
    
    updated_paired_spreadsheet.drop([11], inplace=True)
    
    return updated_paired_spreadsheet


def new_paired_spreadsheet(old_spreadsheet, updated_paired_spreadsheet):
    """Returns a spreadsheet of new paired bets that need to be added 
       to an old spreadsheet."""
    
    # 2 accounts for the missing bets that arent't in individual/paired bet files
    first_new_bet = old_spreadsheet['Profit ID'].nunique() - 2
    new_paired_bets = updated_paired_spreadsheet.iloc[first_new_bet:, ]
    
    return new_paired_bets

## Combine new paired and individual bets

def fill_bet_result_NaN(new_bets_spreadsheet):
    """Sets the bet result of new bets to be unsettled."""

    new_bets_spreadsheet.loc[:, 'Bet Result'].fillna('Unsettled', inplace=True)
    
    return new_bets_spreadsheet

## Settle bets

def recalculate_running_profit(spreadsheet):
    """Need to recalculate running profit after new bets have 
       been settled."""
    
    new_running_profit = spreadsheet.loc[:, 'Profit'].cumsum()
    spreadsheet.loc[:, 'Running Profit'] = new_running_profit
    
    return spreadsheet
