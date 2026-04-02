from nba_api.stats.endpoints import TeamDashboardByShootingSplits, LeagueDashTeamShotLocations, LeagueDashTeamStats
from nba_api.stats.static import teams
from get_multipliers import main as get_mult
import pandas as pd
import time
from datetime import date
pd.set_option('display.precision', 2)

def main(num_games, multipliers_df):

    team = teams.get_teams()
    team_id_list = [[i['id'],i['abbreviation']] for i in team]
    team_id_df = pd.DataFrame(team_id_list, columns=['TEAM_ID', "Team"])
    # team = team_id_list[1][0]
    # team2 = team_id_df[1][0]


    # for id, abbv in team_id_list:
    #     shooting = TeamDashboardByShootingSplits(team_id=id)
    #     shooting_df = shooting.get_data_frames()[0]
    #     master_df[abbv] = shooting_df.T


    # shot_locations = LeagueDashTeamShotLocations(season='2025-26', distance_range='By Zone', last_n_games=num_games)
    # shot_loc_df = shot_locations.get_data_frames()[0]
    # '''MultiIndex([(                     '',   'TEAM_ID'),
    #             (                     '', 'TEAM_NAME'),
    #             (      'Restricted Area',       'FGM'),
    #             (      'Restricted Area',       'FGA'),
    #             (      'Restricted Area',    'FG_PCT'),
    #             ('In The Paint (Non-RA)',       'FGM'),
    #             ('In The Paint (Non-RA)',       'FGA'),
    #             ('In The Paint (Non-RA)',    'FG_PCT'),
    #             (            'Mid-Range',       'FGM'),
    #             (            'Mid-Range',       'FGA'),
    #             (            'Mid-Range',    'FG_PCT'),
    #             (        'Left Corner 3',       'FGM'),
    #             (        'Left Corner 3',       'FGA'),
    #             (        'Left Corner 3',    'FG_PCT'),
    #             (       'Right Corner 3',       'FGM'),
    #             (       'Right Corner 3',       'FGA'),
    #             (       'Right Corner 3',    'FG_PCT'),
    #             (    'Above the Break 3',       'FGM'),
    #             (    'Above the Break 3',       'FGA'),
    #             (    'Above the Break 3',    'FG_PCT'),
    #             (            'Backcourt',       'FGM'),
    #             (            'Backcourt',       'FGA'),
    #             (            'Backcourt',    'FG_PCT'),
    #             (             'Corner 3',       'FGM'),
    #             (             'Corner 3',       'FGA'),
    #             (             'Corner 3',    'FG_PCT')],
    #            names=['SHOT_CATEGORY', 'columns'])'''


    # master_df = pd.DataFrame()
    # for key1,key2 in shot_loc_df.columns:
    #     x = str(key2)
    #     if x in ['TEAM_ID','TEAM_NAME']:
    #         master_df[x] = shot_loc_df[(key1,x)]
    #     elif str(key1) == "Backcourt":
    #         continue
    #     else:
    #         min = shot_loc_df[(key1,x)].min()
    #         max = shot_loc_df[(key1,x)].max()
    #         master_df[(key1,x)] = (shot_loc_df[(key1,x)]-min) / (max - min)

    # master_df['SHOOTING_SCORE'] = master_df.iloc[:,2:].sum(axis=1)




        
    get_season = '2025-26'
    mode = 'PerGame'
    measure = ''

    def get_league_dash(get_season, mode, measure, num_games):
        if measure:
            df = LeagueDashTeamStats(season=get_season, 
                                        per_mode_detailed=mode, 
                                        measure_type_detailed_defense=measure,
                                        last_n_games= num_games)
        else:
            df = LeagueDashTeamStats(season=get_season, 
                                        per_mode_detailed=mode, 
                                        last_n_games= num_games)

        df = df.get_data_frames()[0]
        return df

    td_df = get_league_dash(get_season, mode,'', num_games)
    '''['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA',
        'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
        'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS',
        'PLUS_MINUS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK',
        'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK',
        'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK',
        'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK',
        'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK']'''

    td_df = td_df[['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA',
        'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',  'PTS',
        'PLUS_MINUS']]

    td_adv_df = get_league_dash(get_season, mode,'Advanced', num_games)
    '''['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'E_OFF_RATING',
        'OFF_RATING', 'E_DEF_RATING', 'DEF_RATING', 'E_NET_RATING',
        'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT',
        'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'E_PACE', 'PACE',
        'PACE_PER40', 'POSS', 'PIE', 'GP_RANK', 'W_RANK', 'L_RANK',
        'W_PCT_RANK', 'MIN_RANK', 'OFF_RATING_RANK', 'DEF_RATING_RANK',
        'NET_RATING_RANK', 'AST_PCT_RANK', 'AST_TO_RANK', 'AST_RATIO_RANK',
        'OREB_PCT_RANK', 'DREB_PCT_RANK', 'REB_PCT_RANK', 'TM_TOV_PCT_RANK',
        'EFG_PCT_RANK', 'TS_PCT_RANK', 'PACE_RANK', 'PIE_RANK']'''
    td_adv_df = td_adv_df[['TEAM_ID', 'EFG_PCT', 'TS_PCT']]
    
    dash_master_df = team_id_df
    dash_master_df = pd.merge(team_id_df,td_df, on='TEAM_ID', how= 'outer')
    dash_master_df = pd.merge(dash_master_df, td_adv_df, on='TEAM_ID', how='outer')
    
    '''['TEAM_ID', 'Team', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM',
       'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
       'PTS', 'PLUS_MINUS', 'EFG_PCT', 'TS_PCT']'''
    
    scaled_df = pd.DataFrame()
    for i in dash_master_df.columns:
        mult = multipliers_df[i].tolist()[3] if i in multipliers_df.columns else 1
        if i in ['TEAM_ID', 'Team', 'TEAM_NAME','GP']:
            scaled_df[i] = dash_master_df[i]
        else:
            min = dash_master_df[i].min()
            max = dash_master_df[i].max()
            scaled_df[i] = ((dash_master_df[i]-min)/(max-min))*mult
            
    scaled_df['SHOOTING_SCORE'] = scaled_df.iloc[:, 8:].sum(axis=1)

    today = date.today()
    filename = f'./csv_logs/scaled_shooting_matrix_{today}'
    scaled_df.to_csv(filename, index = False)
    return dash_master_df, scaled_df

if __name__ == '__main__':
    multipliers_df, df_dict = get_mult('Shooting')
    num_games = '0'
    dash_master_df, scaled_df= main(num_games, multipliers_df)
    print(scaled_df)
