from get_main_dataframe import main as get_df_dict
from minmax import minmax
from nba_api.stats.static import teams
import pandas as pd

def main(ngames,df_dict):
    team = teams.get_teams()
    team_id_list = [i['abbreviation'] for i in team]

    # ngames_df_for_merge= pd.DataFrame({'team' : team_id_list})

    def get_last_ngames(ngames,  df_dict = df_dict, team = None):
        if team:
            return df_dict[team].iloc[:ngames,:]
        else:
            temp_dict = {}
            for key in df_dict.keys():
                temp_dict[key] = df_dict[key].iloc[:ngames,:]
            return temp_dict
    
    #dictionary of dataframes with abbv as keys, last n games
    ngames_dict = get_last_ngames(ngames,df_dict)

    for key in ngames_dict.keys():
        ngames_dict[key] = ngames_dict[key].iloc[:,9:].mean()

    ngames_df = pd.DataFrame(ngames_dict).T.reset_index(names=['Team'])

    scaled_ngames = pd.DataFrame({'Team': ngames_df['Team']})
    for i in ngames_df.columns[1:]:
        scaled_ngames[i] = minmax(i, ngames_df)
    
    return scaled_ngames
if __name__ == '__main__':

    df_master, df_dict = get_df_dict()
    '''['SEASON_YEAR', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID',
        'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
        'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
        'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS',
        'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB', 'PTS_PAINT',
        'OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB', 'OPP_PTS_PAINT',
        'E_OFF_RATING', 'OFF_RATING', 'E_DEF_RATING', 'DEF_RATING',
        'E_NET_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO', 'AST_RATIO',
        'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT',
        'E_PACE', 'PACE', 'PACE_PER40', 'POSS', 'PIE', 'OPP_FGM', 'OPP_FGA',
        'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT', 'OPP_FTM',
        'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_REB', 'OPP_AST',
        'OPP_TOV', 'OPP_STL', 'OPP_BLK', 'OPP_BLKA', 'OPP_PF', 'OPP_PFD',
        'OPP_PTS', 'OPP_PFD1']'''
    
    ngames = 10
    scaled_ngames = main(ngames, df_dict)

