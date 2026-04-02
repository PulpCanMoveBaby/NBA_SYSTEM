from nba_api.stats.endpoints import TeamGameLogs
from nba_api.stats.static import teams
from minmax import minmax

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

        filename = f"./csv_logs/team_game_logs_{measure}_{season}.csv"

        df_team_logs.to_csv(filename, index=False)
        return df_team_logs

    df_master = pd.DataFrame()
    df_team_logs = get_logs(season, measure, season_type)
    df_team_logs_misc = get_logs(season, 'Misc', season_type)
    df_team_logs_adv = get_logs(season, 'Advanced', season_type)
    df_team_logs_opp = get_logs(season, 'Opponent', season_type)
    
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

    def remove_rank_cols(df):
        remove_cols = []
        for col in df.columns:
            if col[-4:] == "RANK" or col == 'AVAILABLE_FLAG':
                remove_cols.append(col)
        df = df.drop(columns=remove_cols)
        return df

    df_master = df_team_logs
    
    for df in df_list:
        df_master = drop_common_and_concat(df_master, df)

    df_master = remove_rank_cols(df_master)

    filename = f"./csv_logs/team_game_logs_MASTER.csv"
    df_master.to_csv(filename, index=False)
    
    team = teams.get_teams()
    team_id_list = [i['abbreviation'] for i in team]
    df_dict = {name: df_master[df_master['TEAM_ABBREVIATION'] == name] for name in team_id_list}
    
    for key in df_dict.keys():
        df_dict[key] = df_dict[key].sort_values(by='GAME_DATE', ascending=False)
    
    def get_last_ngames(ngames, team = None, df_dict = df_dict):
        # ngames = 8
        if team:
            return df_dict[team].iloc[:ngames,:]
        else:
            temp_dict = {}
            for key in df_dict.keys():
                temp_dict[key] = df_dict[key].iloc[:ngames,:]
            return temp_dict

    return df_master, df_dict

if __name__ == '__main__':
    df_master, df_dict = main()