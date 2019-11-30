"""These are functions that were made in part 3 to keep track of money across
   various accounts with bookmakers."""

def qualifying_bet_balances(spreadsheet):
    """Returns a series with the balance for each bookie due to all 
       settled qualifying bets."""
    
    winning_qualifying_bets = (spreadsheet['Bet Type'] == 'Qualifying')   \
                               & (spreadsheet['Bet Result'] == 'Win')
    
    qualifying_by_bookie = spreadsheet[winning_qualifying_bets].groupby('Bookie') 
    
    # Our original stake is returned with qualifying bets
    qualifying_balances = qualifying_by_bookie['Stake'].sum()   \
                             + qualifying_by_bookie['Return'].sum()
    
    # Smarkets balance will be calculated separately 
    if 'Smarkets' in qualifying_balances.index:
        qualifying_balances.drop('Smarkets', inplace=True)
        
    return qualifying_balances


def free_bet_balances(spreadsheet):
    """Returns a series with the balance for each bookie due to all 
       settled free bets."""

    winning_free_bets = (spreadsheet['Bet Type'] == 'Free (SNR)') \
                               & (spreadsheet['Bet Result'] == 'Win')
    
    free_by_bookie = spreadsheet[winning_free_bets].groupby('Bookie')
    
    # Our original state is not returned with free bets
    # SNR means "stake not returned"
    free_balances = free_by_bookie['Return'].sum()
    
    # Smarkets balance will be calculated separately 
    if 'Smarkets' in free_balances.index:
        free_balances.drop('Smarkets', inplace=True)
    
    return free_balances


def add_series(series_1, series_2):
    """Removes NaNs when two series are added together and some indices don't match.
       Indices which don't match keep values from original series.
       Still works if all indices from both series match."""
    
    potential_sum = series_1 + series_2
    
    removed_NaN_sum = potential_sum.fillna(series_1)  \
                                   .fillna(series_2)
    return removed_NaN_sum


def bookie_balances(spreadsheet):
    """Returns the total balance for each bookmaker for all settled bets."""
    
    return add_series(qualifying_bet_balances(spreadsheet), free_bet_balances(spreadsheet))


def value_index_list(series):
    """Iterates through values in a pandas series and returns a dictionary of the form
       {value : [indices for value]}

       Originally used to calculate qualifying bet balances before I realised that it was
       easier to use groupby instead.

       Could be useful in the future."""

    value_indices_dictionary = {}

    for index, value in series.iteritems():
        value_indices_dictionary.setdefault(value, []).append(index)

    return value_indices_dictionary
