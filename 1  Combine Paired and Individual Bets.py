import pandas as pd


# Read csv files
paired_bets_file = 'file path/Paired\ Bets.csv'
paired_bets_file = paired_bets_file.replace("\\", "")
paired_bets = pd.read_csv(paired_bets_file)

individual_bets_file = 'file path/Individual\ Bets.csv'
individual_bets_file = individual_bets_file.replace("\\", "")
individual_bets = pd.read_csv(individual_bets_file)


# Remove unwanted columns from individual_bets
individual_bets.drop(['BookieID', 'BetOutcomeID', 'BettingTypeID', 'ItemID'], axis=1, inplace=True)


# Rename first column of individual_bets to match first column of paired_bets
individual_bets.rename(columns={'profitid':'ProfitID'}, inplace=True)


# Take columns from paired_bets and merge to individual_bets on matching ProfitIDs
bet_spreadsheet = individual_bets

for column in ['sport', 'Event', 'EventTime', 'datecreated ', 'BetType', 'Note']:
    partially_merged = pd.merge(bet_spreadsheet, paired_bets.loc[:,['ProfitID',column]], 
                                on='ProfitID')
    bet_spreadsheet = partially_merged

    
# Rename columns
bet_spreadsheet.columns = ['Profit ID', 'Bookie', 'Bet Result', 'Type', 'Outcome', 'Stake',
                           'Odds', 'Fee (%)', 'Liability', 'Return', 'Potential Profit', 
                           'Sport', 'Event', 'Event Time', 'Date Created', 'Bet Type', 'Note']


# Change order of columns
columns_reordered = ['Date Created', 'Sport', 'Event', 'Event Time', 'Bookie','Bet Type',
                     'Type', 'Outcome', 'Stake', 'Odds', 'Fee (%)', 'Liability', 'Return',
                     'Potential Profit', 'Bet Result', 'Note', 'Profit ID']

bet_spreadsheet = bet_spreadsheet.loc[:, columns_reordered]


# Use the term 'Qualifying' instead of 'Normal'
bet_spreadsheet.loc[:,'Bet Type'].replace('Normal', 'Qualifying', inplace=True)


# Add which bets won and lost
win_index = [0,2,5,6,9,10,13,15]
lose_index = list(set(range(16)) - set(win_index))

bet_spreadsheet.loc[win_index,'Bet Result'] = "Win"
bet_spreadsheet.loc[lose_index,"Bet Result"] = "Lose"


#Replace NaNs in notes with empty strings
bet_spreadsheet.fillna('', inplace=True)


# Save new spreadsheet
bet_spreadsheet.to_csv('Bet Spreadsheet.csv', index=False)


