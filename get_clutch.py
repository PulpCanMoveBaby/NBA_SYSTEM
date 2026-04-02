from nba_api.stats.endpoints import LeagueDashTeamClutch
from nba_api.stats.static import teams
import pandas as pd
import sys, os
cwd = os.getcwd()

measure = 'Advanced'
season = '2025-26'
season_type = 'Regular Season'
mode = 'PerMinute'

def main():
    team_list = teams.get_teams()
    clutch_advanced = LeagueDashTeamClutch(season=season, per_mode_detailed=mode)
    df_clutch_advanced = clutch_advanced.get_data_frames()[0]
    abbv_df = pd.DataFrame()
    team_abbv = [[i['abbreviation'],i['full_name']] for i in team_list]
    abbv_df = pd.DataFrame({'Team':[i[0] for i in team_abbv], 'TEAM_NAME':[i[1] if i[1] != 'Los Angeles Clippers' else 'LA Clippers' for i in team_abbv]})
    # abbv_df['TEAM_NAME'] = df_clutch_advanced['TEAM_NAME'] 
    rank_cols = []
    for i in df_clutch_advanced.columns:
        if i[-4:] == 'RANK':
            rank_cols.append(i)

    df_clutch_advanced =  df_clutch_advanced.drop(columns=rank_cols)
    df_clutch_advanced = pd.merge(df_clutch_advanced,abbv_df, on='TEAM_NAME', how='outer')
    # print(df_clutch_advanced)

    # ['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA',
    #        'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
    #        'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS',
    #        'PLUS_MINUS']

    temp_df = pd.DataFrame()
    temp_df['Team'] = df_clutch_advanced['Team']
    temp_df['clutch_mins'] = df_clutch_advanced['MIN']
    temp_df = temp_df.sort_values(by='clutch_mins', ascending=True).reset_index(drop=True)
    temp_df['clutch_potential'] = list(range(1,31))

    stats = ['FGM', 'FGA','FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
        'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS',
        'PLUS_MINUS']

    less_is_better = ['TOV', 'PF', 'BLKA']

    clutch_matrix =pd.DataFrame()

    for i in df_clutch_advanced.columns:
        if i in stats:
            max_col = df_clutch_advanced[i].max()
            min_col = df_clutch_advanced[i].min()
            if i in less_is_better:
                clutch_matrix[str(i)] = 1-(df_clutch_advanced[i]-min_col)/(max_col-min_col)
            else:
                clutch_matrix[str(i)] = (df_clutch_advanced[i]-min_col)/(max_col-min_col)

    clutch_matrix['score'] = clutch_matrix.sum(axis=1)
            
            
    clutch_matrix['Team'] = df_clutch_advanced['Team']

    # print(clutch_matrix)

    master_df = pd.merge(df_clutch_advanced[['Team', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT']],clutch_matrix[['score', 'Team']], on='Team', how='outer' )
    master_df = pd.merge(master_df, temp_df, on='Team', how='outer')
    master_df['CLUTCH_SCORE'] = master_df['score']*(master_df['W_PCT'])+master_df['clutch_potential']/5
    master_df.sort_values(by='CLUTCH_SCORE', ascending=False , inplace=True)
    # master_df['CLUTCH_RANK'] = list(range(1,31))
    # print(master_df)

    filename = f'./csv_logs/clutch_score.csv'
    master_df.to_csv(filename, index=False)
    return master_df

if __name__ == '__main__':
    x = main()