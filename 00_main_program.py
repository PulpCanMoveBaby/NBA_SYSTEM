
from get_main_dataframe import main as get_df_dict
from nba_api.stats.static import teams
import get_scores_v3

#GET MASTER DATA========================================
team = teams.get_teams()
team_id_list = [i['abbreviation'] for i in team]

while True:
    try:
        df_master, df_dict = get_df_dict()
        matchups = get_scores_v3.get_today_matchups()
        print("Got the master data successfully...")
        break
    except:
        print("Connection took too long, trying again...")

if df_dict:
    import get_yesterdays_results
    import optimize_PIE

#THIS IS THE GET SCORES CODE=============================
games = list(range(7,11))
master_df = get_scores_v3.main(games, df_dict=df_dict, df_master=df_master)
get_scores_v3.get_matchup(matchups, master_df)