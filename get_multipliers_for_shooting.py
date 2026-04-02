from nba_api.stats.endpoints import LeagueGameFinder, TeamGameLog, TeamGameLogs, LeagueHustleStatsTeam
from nba_api.stats.static import teams
import pandas as pd

def main():
    measure = ''
    season = '2025-26'
    season_type = 'Regular Season'

    team = teams.get_teams()

    def get_logs(season, measure, season_type):
        team_logs = TeamGameLogs(
                                season_nullable=season,
                                measure_type_player_game_logs_nullable= measure,
                                season_type_nullable=season_type
                                )
        # print(team_logs)
        df_team_logs = team_logs.get_data_frames()[0]
        df_team_logs['WL'] = [1 if i == 'W' else 0 for i in df_team_logs['WL']]
        # print(df_team_logs['WL'])

        filename = f".csv_logs/team_game_logs_{measure}_{season}.csv"

        df_team_logs.to_csv(filename, index=False)
        return df_team_logs

    df_master = pd.DataFrame()
    df_team_logs = get_logs(season, measure, season_type)
    df_team_logs_misc = get_logs(season, 'Misc', season_type)
    df_team_logs_adv = get_logs(season, 'Advanced', season_type)
    df_team_logs_opp = get_logs(season, 'Opponent', season_type)
    
    
    # hustle = LeagueHustleStatsTeam(season=season)
    # df_team_logs_hustle = hustle.get_data_frames()[0]
    
    
    df_list = [df_team_logs_misc, df_team_logs_adv, df_team_logs_opp]


    def drop_common_and_concat(df1, df2):
        common_cols = []
        df2 = df2.sort_values(by=['GAME_ID', 'WL'], ascending=False).reset_index(drop=True)
        df1 = df1.sort_values(by=['GAME_ID', 'WL'], ascending=False).reset_index(drop=True)
        for col in df1.columns:
            if col in df2.columns:
                common_cols.append(col)
        df2.drop(columns=common_cols, inplace=True)
        df1 = pd.concat([df1,df2], axis=1)
        return df1

    # def merge_dfs(df1, df2):
    #     merged_df = pd.merge(df1,df2, on='GAME_ID', how='outer')
    #     return merged_df


    def remove_rank_cols(df):
        remove_cols = []
        for col in df.columns:
            if col[-4:] == "RANK":
                remove_cols.append(col)
        df = df.drop(columns=remove_cols)
        return df

    df_master = df_team_logs
    
    for df in df_list:
        df_master = drop_common_and_concat(df_master, df)

    # for df in df_list:
    #     df_master = merge_dfs(df_master, df)

    df_master = remove_rank_cols(df_master)

    filename = f".csv_logs/team_game_logs_MASTER.csv"
    df_master.to_csv(filename, index=False)

    df_team_logs = df_team_logs.join(df_team_logs_misc[['PTS_PAINT', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB']])

    game_ids = list(set(df_master["GAME_ID"]))
    # print(game_ids)
    print(len(game_ids))

    master_list_basic = ['WL','FGA', 'NET_RATING',
        'FG3A', 'FTA', 'OREB', 'DREB', 'REB', 'AST',
        'TOV', 'STL', 'BLK', 'PF','PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
        'PTS_PAINT', 'AST_PCT', 'AST_TO',
        'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT',
        'TS_PCT', 'PACE', 'POSS']
    
    # master_list_basic_unedited = ['WL', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
    #     'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
    #     'TOV', 'STL', 'BLK', 'PF', 'PTS', 'PLUS_MINUS',
    #     'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
    #     'PTS_PAINT','OFF_RATING','DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO',
    #     'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT',
    #     'TS_PCT', 'PACE', 'POSS', 'PIE']


    master_list_defense = ['WL', 'FGM', 'FGA', 'FG_PCT', 'FG3M',
       'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
       'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
       'PTS_PAINT', 'OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB',
       'OPP_PTS_PAINT','OFF_RATING', 'DEF_RATING', 'NET_RATING', 'AST_PCT', 'AST_TO',
       'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT',
       'TS_PCT','PACE','POSS', 'PIE', 'OPP_FGM', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT',
       'OPP_FTM', 'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_REB',
       'OPP_AST', 'OPP_TOV', 'OPP_STL', 'OPP_BLK', 'OPP_BLKA', 'OPP_PF',
       'OPP_PFD', 'OPP_PTS']
    
    #editing idea is to remove anything that is just the opposite, eliminating redundant multipliers
    #also current strategy is to account for what teams can control, attempts not makes, and OPP makes not attempts

    #netRating and PIE go back in here if necessary and all removed stats
    # master_list_defense = ['NET_RATING','PIE','WL','FGA',
    #    'FG3A','FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'AST_TO',
    #    'TOV', 'STL', 'BLK', 'PF','PTS_OFF_TOV', 'PTS_2ND_CHANCE', 'PTS_FB',
    #    'PTS_PAINT', 'OREB_PCT', 'DREB_PCT', 'REB_PCT','POSS','OPP_FG3M',
    #    'OPP_FTA', 'OPP_OREB', 'OPP_DREB', 'OPP_REB', 'OPP_TOV', 'OPP_STL', 'OPP_BLK','OPP_PF','OPP_PTS']
    
    # master_from_boats_matrix = ['CONTESTED_SHOTS','DEFLECTIONS', 'CHARGES_DRAWN','LOOSE_BALLS_RECOVERED','BOX_OUTS']
    
    # master_after_compare = [i for i in master_from_boats_matrix if i not in master_list_defense]
    

    master_list = master_list_defense

    master_dict = {key: [0,0,0] for key in master_list}
    # master_dict.update({key: [1,1,1] for key in master_after_compare})

    count = 0
    for game in game_ids:
        matchup = df_master[df_master['GAME_ID'] == game]
        for key in matchup.columns:
            if key in master_dict.keys():
                if float(matchup[key].diff(periods = -1).iloc[0]) > 0:
                    master_dict[key][0] += 1
                # elif float(matchup[key].diff(periods = -1).iloc[0]) > 0 and key == 'OPP_PTS':
                #     master_dict[key][0] += 1
                #     count +=1
                # elif float(matchup[key].diff(periods = -1).iloc[0]) < 0 and key == 'NET_RATING':
                #     master_dict[key][1] += 1
                #     count +=1
                elif float(matchup[key].diff(periods = -1).iloc[0]) < 0:
                    master_dict[key][1] += 1
                
                else:
                    master_dict[key][2] += 1    

    less_is_better = ['TOV', 'BLKA', 'PF','OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB',
       'OPP_PTS_PAINT','DEF_RATING','TM_TOV_PCT', 'OPP_FGM', 'OPP_FGA', 'OPP_FG_PCT', 'OPP_FG3M', 'OPP_FG3A', 'OPP_FG3_PCT',
       'OPP_FTM', 'OPP_FTA', 'OPP_FT_PCT', 'OPP_OREB', 'OPP_DREB', 'OPP_REB',
       'OPP_AST', 'OPP_TOV', 'OPP_STL', 'OPP_BLK','OPP_PFD', 'OPP_PTS']
    # less_is_better = ['TOV', 'PF', 'DEF_RATING','TM_TOV_PCT']


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

    # master_dict['NET_RATING'][3] = master_dict['NET_RATING'][3]/2 

    multipliers_df = pd.DataFrame(master_dict)
    filename = f"./csv_logs/get_multipliers2.csv"
    multipliers_df.to_csv(filename, index=False)
    # print(multipliers_df)
    # print(master_dict) 
    return multipliers_df, master_dict, df_master  

if __name__ == '__main__':
    count = 0
    if count == 0:
        multipliers_df, master_dict, df_master  = main()

    