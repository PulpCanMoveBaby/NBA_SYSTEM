#! /usr/bin/env python3


import nba_api.stats.endpoints as nba
import pandas as pd
from nba_api.stats.static import teams

team_info = teams.get_teams()
team_abbv = [[i['abbreviation'],i["full_name"]] for i in team_info]
team_abbv = sorted(team_abbv, key=lambda x : x[1])
team_ab = [i[0] for i in team_abbv]
team_name = [i[1] if i[1] != 'Los Angeles Clippers' else 'LA Clippers' for i in team_abbv]
td_team_abbv = pd.DataFrame({'Team': team_ab, 'TEAM_NAME': team_name})

traditional_total = nba.leaguedashteamstats.LeagueDashTeamStats(season="2025-26")

td_df = traditional_total.get_data_frames()[0]

win_perc_df = pd.DataFrame()
win_perc_df = pd.merge(td_team_abbv, td_df[['TEAM_NAME','W_PCT']], on='TEAM_NAME')
win_perc_df = win_perc_df.drop(columns='TEAM_NAME')
