from get_main_dataframe import main as get_main_dataframe
import pandas as pd

def main(mode = None, predict=False, df_dict=None, df_master=None):
    if df_dict is None:
        df_master, df_dict = get_main_dataframe()
    
    game_ids = list(set(df_master["GAME_ID"]))
    # print(game_ids)
    print(len(game_ids))

    filename = f'./optimize_pie.csv'
    pie_data = pd.read_csv(filename)
    pie_data = pd.DataFrame(pie_data)

    master_list_basic = ['WL','FGA', 'NET_RATING',
        'FG3A', 'FTA', 'OREB', 'DREB', 'REB', 'AST',
        'TOV', 'STL', 'BLK', 'PF','PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
        'PTS_PAINT', 'AST_PCT', 'AST_TO',
        'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT',
        'TS_PCT', 'PACE', 'POSS']

    '''
        FULL LIST OF COLUMNS IN df_master======================================================
        ['SEASON_YEAR', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID',
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
        'OPP_PTS', 'OPP_PFD1']
        FULL LIST OF COLUMNS IN df_master======================================================
        '''

    # columns_master_edited = ['WL', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
    #    'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
    #    'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
    #    'PTS_PAINT', 'OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB',
    #    'OPP_PTS_PAINT','OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO',
    #    'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT',
    #    'TS_PCT','PACE','POSS', 'PIE', 'OPP_FGM', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT',
    #    'OPP_FTM', 'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_REB',
    #    'OPP_AST', 'OPP_TOV', 'OPP_STL', 'OPP_BLK', 'OPP_BLKA', 'OPP_PF',
    #    'OPP_PFD', 'OPP_PTS', 'OPP_PFD1']
    
    #editing idea is to remove anything that is just the opposite, eliminating redundant multipliers
    #also current strategy is to account for what teams can control, attempts not makes, and OPP makes not attempts

    #netRating and PIE go back in here if necessary and all removed stats
    master_list= ['NET_RATING','PIE','FGA',
       'FG3A','FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'AST_TO',
       'TOV', 'STL', 'BLK', 'PF','PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
       'PTS_PAINT', 'OREB_PCT', 'DREB_PCT', 'REB_PCT','POSS','OPP_FG3M',
       'OPP_FTA', 'OPP_OREB', 'OPP_DREB', 'OPP_REB', 'OPP_TOV', 'OPP_STL', 'OPP_BLK','OPP_PF','OPP_PTS']
    
    if mode == 'Shooting':
            master_list = ['FGM', 'FGA', 'FG_PCT', 'FG3M',
       'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT','PTS', 'EFG_PCT',
       'TS_PCT']
            
    if mode == 'Defense':
            master_list  = ['STL', 'BLK', 'PTS_OFF_TOV', 'OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB',
       'OPP_PTS_PAINT', 'DEF_RATING', 'OPP_FGM', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT',
       'OPP_FTM', 'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_REB',
       'OPP_AST', 'OPP_TOV', 'OPP_PTS']
    

    master_dict = {key: [0,0,0] for key in master_list}

    count = 0
    for game in game_ids:
        if isinstance(game,str):
            matchup = df_master[df_master['GAME_ID'] == game]
            for key in matchup.columns:
                if key in master_dict.keys():
                    if float(matchup[key].diff(periods = -1).iloc[0]) > 0:
                        master_dict[key][0] += 1

                    elif float(matchup[key].diff(periods = -1).iloc[0]) < 0:
                        master_dict[key][1] += 1
                    
                    else:
                        master_dict[key][2] += 1  
    #UNCHANGE THIS IF PROBLEMS OCCUR, TRIED TO DO A GENERAL LESS IS BETTER FILTERED BY COLS IN MASTER LIST
    # less_is_better = ['TOV','PF','TM_TOV_PCT','OPP_FGM','OPP_FG3M',
    #    'OPP_FTA','OPP_OREB', 'OPP_DREB', 'OPP_REB', 'OPP_STL', 'OPP_BLK', 'OPP_PTS']
    
    less_is_better = ['TOV', 'BLKA', 'PF','OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB', 'OPP_PTS_PAINT',
        'DEF_RATING','TM_TOV_PCT', 'OPP_FGM', 'OPP_FGA',
        'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT', 'OPP_FTM',
        'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_REB', 'OPP_AST',
        'OPP_STL', 'OPP_BLK','OPP_PFD',
        'OPP_PTS', 'OPP_PFD1']

    if predict == False:
        manual_score = {'NET_RATING': [int(pie_data.iloc[1,0])], 'PIE': [int(pie_data.iloc[1,2])], 'OPP_PTS':[0]}
    else:
        manual_score = {'NET_RATING': [7], 'PIE': [5], 'OPP_PTS':[6]}

    for key, values in master_dict.items():
        if key == 'WL':
            master_dict[key] = values+[0]
        else:
            if key in manual_score.keys():
                master_dict[key] = values + manual_score[key]
            
            elif key in less_is_better:
                if values[0] == 0:
                    master_dict[key] = values+[0]
                else:
                    master_dict[key] = values+[round(values[1]/values[0],3)]
            
            else:
                if values[1] == 0:
                    master_dict[key] = values+[0]
                else:
                    master_dict[key] = values+[round(values[0]/values[1],3)]


    multipliers_df = pd.DataFrame(master_dict)
    filename = f"./multiplier_dictionary.csv"
    multipliers_df.to_csv(filename, index=False)

    # if mode == 'Shooting':
    #     return multipliers_df
    # elif mode == 'multipliers':
    #     return multipliers_df
    if __name__ == '__main__':
        return multipliers_df, master_dict, df_dict, df_master
    else:
        return multipliers_df
    

if __name__ == '__main__':
    #multipliers_df and master_dict are specifically for the coefficients
    #df_dict is the main dictionary that holds all the relevant stats by team
    #df_master is the main dataframe that holds all the relevant stats for each team for each game
    multipliers_df, master_dict, df_dict, df_master = main()

    