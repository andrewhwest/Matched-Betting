"""Require this function to calculate account balances for each bookmaker. 
   Generalised its syntax as it could be extremely useful and commonly used for work with future dataframes."""

def value_index_list(series):
    """Iterates through values in a pandas series and returns a dictionary of the form
       {value : [indices for value]}"""

    value_indices_dictionary = {}

    for index, value in series.iteritems():
        value_indices_dictionary.setdefault(value, []).append(index)

    return value_indices_dictionary
