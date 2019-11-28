""""My first 4 matched bets were missing from my bet spreadsheet.
    This adds them in to the spreadsheet and provides a template for adding in future bets that are 
    missing."""

import pandas as pd


bet_spreadsheet = pd.read_csv('Bet Spreadsheet.csv')

# Make a copy of the first 4 rows and insert them as the first 4 rows 
bet_spreadsheet = pd.concat([bet_spreadsheet.iloc[:4, ], bet_spreadsheet], ignore_index=True)

## Add first pair of missing bets to rows 0 and 1

# Change values that apply to the first pair of Back and Lay bets
bet_spreadsheet.iloc[:2, [0, 2, 3, 5, 7, 16]] = ['19/11/2019 13:48:04', 
                                                 'Brighton and Hove Albion v Leicester', 
                                                 '23/11/2019 15:00:00', 'Qualifying', 
                                                 'Leicester', 7967100]

# Change values that are specific to each bet
bet_spreadsheet.iloc[0, [4, 8, 9, 12, 13]] = ['Betfred', 10.00, 2.05, 10.50, -0.43]
bet_spreadsheet.iloc[1, [8, 9, 11, 12, 13]] = [9.76, 2.12, 10.93, 9.56, -0.44]

## Add second pair of missing bets to rows 2 and 3

# Change values that apply to the second pair of Back and Lay bets
bet_spreadsheet.iloc[2:4, [0, 2, 3, 5, 7, 16]] = ['19/11/2019 14:27:29', 'Rochdale v Wrexham', 
                                                  '19/11/2019 19:45:00', 'Qualifying', 
                                                  'Rochdale', 7967200]

# Change values that are specific to each bet
bet_spreadsheet.iloc[2, [4, 8, 9, 12, 13]] = ['Coral', 5.00, 1.91, 4.55, -0.1]
bet_spreadsheet.iloc[3, [8, 9, 11, 12, 13]] = [5.00, 1.93, 4.65, 4.90, -0.1]

# Save changes
bet_spreadsheet.to_csv('Bet Spreadsheet with missing bets added.csv', index=False)
