from nba_api.stats.endpoints import  LeagueHustleStatsTeam
from nba_api.stats.static import teams
import pandas as pd
import time
pd.set_option('display.precision', 2)



def main():
    measure = ''
    season = '2025-26'
    season_type = 'Regular Season'

    team = teams.get_teams()
    team_id_list = [[i['id'],i['abbreviation']] for i in team]
    team_id_df = pd.DataFrame(team_id_list, columns=['TEAM_ID', "Team"])


    hustle = LeagueHustleStatsTeam(season=season, per_mode_time='PerGame')
    hustle_df = hustle.get_data_frames()[0]

    mean_matrix = pd.DataFrame()
    for key in hustle_df.columns:
        if key in ['TEAM_ID', 'TEAM_NAME', 'MIN']:
            mean_matrix[key] = hustle_df[key]
        else:
            mean_matrix[key] = hustle_df[key] - hustle_df[key].mean()

    master_df = pd.DataFrame()
    master_df = pd.merge(team_id_df, mean_matrix, on='TEAM_ID', how='outer')

    '''['TEAM_ID', 'Team', 'TEAM_NAME', 'MIN', 'CONTESTED_SHOTS',
       'CONTESTED_SHOTS_2PT', 'CONTESTED_SHOTS_3PT', 'DEFLECTIONS',
       'CHARGES_DRAWN', 'SCREEN_ASSISTS', 'SCREEN_AST_PTS',
       'OFF_LOOSE_BALLS_RECOVERED', 'DEF_LOOSE_BALLS_RECOVERED',
       'LOOSE_BALLS_RECOVERED', 'PCT_LOOSE_BALLS_RECOVERED_OFF',
       'PCT_LOOSE_BALLS_RECOVERED_DEF', 'OFF_BOXOUTS', 'DEF_BOXOUTS',
       'BOX_OUTS', 'PCT_BOX_OUTS_OFF', 'PCT_BOX_OUTS_DEF']'''
    
    master_df = master_df.drop(columns = ['SCREEN_ASSISTS', 'SCREEN_AST_PTS',
       'OFF_LOOSE_BALLS_RECOVERED', 'DEF_LOOSE_BALLS_RECOVERED','PCT_LOOSE_BALLS_RECOVERED_OFF',
       'PCT_LOOSE_BALLS_RECOVERED_DEF', 'PCT_BOX_OUTS_OFF', 'PCT_BOX_OUTS_DEF'])

    # print(master_df.columns)

    master_df['HUSTLE_SCORE'] = master_df.iloc[:, 4:].sum(axis=1)

    filename = f'/home/k/betting_code/hustle_score.csv'
    master_df.to_csv(filename, index=False)
    return master_df


if __name__ == "__main__":
    master_df = main()






