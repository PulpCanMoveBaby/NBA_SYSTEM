from nba_api.stats.endpoints import TeamGameLogs,  PlayByPlayV3
from datetime import  timedelta, date
import pandas as pd
import matplotlib.pyplot as plt
import math
pd.set_option('display.precision', 2)


#READ FILES=====================================================================
# yesterday  = datetime.now() - timedelta(days=1)
filename = f'./today_matchups.csv'
yest_matchups = pd.read_csv(filename)

#write a backup of the matchups with yesterday's date in case we need to reference it later
filename = f'./today_matchups_{date.today()-timedelta(days=1)}.csv'
yest_matchups.to_csv(filename, index=False)

#make the dataframe
yest_matchups = pd.DataFrame(yest_matchups)

filename =f'./prediction_scores_ngames_{date.today()-timedelta(days=1)}.csv'
predictions = pd.read_csv(filename)
prediction_df = pd.DataFrame(predictions)
#READ FILES=====================================================================


change_file = input('Do you want to add to results_tracker totals?? (y) or (n) --> ' )


#DONT CHANGE THIS TO FALSE UNLESS YOU WANT TO RESTART THE DICT========
add_to_dict = True
#DONT CHANGE THIS TO FALSE UNLESS YOU WANT TO RESTART THE DICT========

if add_to_dict:
    filename = f'./results_tracker.csv'
    matchup_dict_df = pd.read_csv(filename, index_col=0)
    matchup_dict = matchup_dict_df.to_dict()

#=====================================================================
#=====================================================================



#GET THE GAMES FROM YESTERDAY==================================================================================================
yest_games = TeamGameLogs(season_nullable='2025-26', last_n_games_nullable='1', season_type_nullable='Regular Season')
yest_games_df = yest_games.get_data_frames()[0]
yesterday = yest_games_df.loc[1, 'GAME_DATE']
yest_games_df = yest_games_df[yest_games_df['GAME_DATE'] == yesterday]
game_ids = set(yest_games_df["GAME_ID"].tolist())
#GET THE GAMES FROM YESTERDAY==================================================================================================


# MAKE LEAD TRACKER CHARTS==================================================
# MAKE LEAD TRACKER CHARTS==================================================
yest_playbyplay_list = []
for gameid in game_ids:
    yest_playbyplay= PlayByPlayV3(gameid).get_data_frames()[0]
    filename = f'./playbyplay.csv'
    yest_playbyplay.to_csv(filename, index = False)

    home_team = yest_playbyplay[yest_playbyplay['location'] == 'h']
    match_home = list(set(home_team['teamTricode'][home_team['teamTricode'] != '']))[0]

    away_team = yest_playbyplay[yest_playbyplay['location'] == 'v']
    match_away = list(set(away_team['teamTricode'][away_team['teamTricode'] != '']))[0]

    match= f'{match_away} @ {match_home}'
    # match = ' vs '.join(match)
    home_score = yest_playbyplay['scoreHome'].tolist()
    home_score = [int(i) for i in home_score if i]
    away_score = yest_playbyplay['scoreAway'].tolist()
    away_score = [int(i) for i in away_score if i]
    diff = [(i-j)*-1 for i,j in zip(home_score,away_score)]
    xs = list(range(len(diff)))
    yest_playbyplay_list.append([match, xs, diff])

'''# Iterate through the games and plot
for i, j in enumerate(yest_playbyplay_list):
    if i < len(axes_flat): # Ensure we don't go out of bounds if there are fewer axes than expected
        ax = axes_flat[i]
        ax.bar(j[1], j[2])
        ax.set_title(j[0]) # Use set_title() method for axes objects'''

cols = 3 if len(yest_playbyplay_list) < 12 else 4
rows = math.ceil(len(yest_playbyplay_list)/cols)
num_games = len(yest_playbyplay_list)
fig, axes = plt.subplots(rows, cols, figsize = (15,10))
axes_flat = axes.flatten()
for i,j in enumerate(yest_playbyplay_list):
    if i > num_games:
        continue
    else:
        ax = axes_flat[i]
        ax.bar(j[1], j[2])
        ax.set_title(j[0])
fig.suptitle("Yesterday's Games --> Away(+) @ Home(-)", fontsize = 16)
plt.tight_layout()
plt.savefig(f'./lead_tracker_{yesterday}')
plt.show
# MAKE LEAD TRACKER CHARTS==================================================
# MAKE LEAD TRACKER CHARTS==================================================


#GET THE RESULTS OF THE MAIN NON PREDICTION CATEGORIES===========================================================
yest_winners_df= yest_games_df[yest_games_df['WL'] == 'W']
yest_winners = yest_winners_df['TEAM_ABBREVIATION'].tolist()
yest_losers_df = yest_games_df[yest_games_df['WL'] == 'L']
yest_losers = yest_losers_df['TEAM_ABBREVIATION'].tolist()
yest_matchups = yest_matchups.drop(list(range(2,yest_matchups.shape[0],3)))
yest_matchups = yest_matchups.reset_index(drop=True)
for i in yest_matchups.columns:
    if i == 'Team':
        yest_matchups[i] = yest_matchups[i]
    else:
        yest_matchups[i] = yest_matchups[i].astype(float)

'''['Team', 'SeasonWin%', 'SeasonWinRank', 'Win%_1', 'Shooting_1',
       'Score_1', 'Rank_1', 'Win%_2', 'Shooting_2', 'Score_2', 'Rank_2',
       'Win%_3', 'Shooting_3', 'Score_3', 'Rank_3', 'Win%_4', 'Shooting_4',
       'Score_4', 'Rank_4', 'Win%_5', 'Shooting_5', 'Score_5', 'Rank_5',
       'Win%_6', 'Shooting_6', 'Score_6', 'Rank_6', 'Win%_7', 'Shooting_7',
       'Score_7', 'Rank_7', 'Win%_8', 'Shooting_8', 'Score_8', 'Rank_8',
       'Win%_9', 'Shooting_9', 'Score_9', 'Rank_9', 'Win%_10', 'Shooting_10',
       'Score_10', 'Rank_10', 'avg_score', 'avg_shooting', 'avg_rank',
       'avg_win%', 'SeasonPull', 'HUSTLE_SCORE', 'CLUTCH_SCORE', 'CONSISTENCY',
       'SCCHS']'''

num_cols = yest_matchups.select_dtypes(include='number').columns
matchups_list = []
rank_cols = ['SeasonWinRank','Rank_1','Rank_2','Rank_3',
                 'Rank_4','Rank_5','Rank_6','Rank_7','Rank_8',
                 'Rank_9', 'Rank_10','avg_rank']

#WRITE CODE TO READ AND WRITE THIS INTO A FILE======
if not add_to_dict:
    matchup_dict = {key:{'W':0, 'L':0, 'T':0} for key in yest_matchups.columns[1:]}
#WRITE CODE TO READ AND WRITE THIS INTO A FILE======

new_keys = ['Prediction_0','Prediction_4', 'Prediction_8', 'Prediction_12', 'SeasonShooting','ShootingPull']
for i in new_keys:
    if i not in matchup_dict.keys():
        matchup_dict[i] = {'W':0, 'L':0, 'T':0}


for i in range(0,yest_matchups.shape[0],2):
    postponed = False
    matchup = yest_matchups.loc[i:i+1,:]
    matchups_list.append(matchup)
    if matchup.iloc[0,0] in yest_winners:
        favorite=True
        stop = 0
    elif matchup.iloc[0,0] in yest_losers:
        favorite=False
        stop = 1
    else:
        postponed = True
    
    if postponed:
        continue
    else:
        if favorite:
            matchup = matchup[num_cols]
            matchup = matchup.diff(periods=-1)
        else:
            matchup = matchup[num_cols]
            matchup = matchup.diff()
        idx = 0
        for j in matchup.columns:
            if j in num_cols:
                if matchup.iloc[stop,idx] < 0 and j in rank_cols:
                    matchup_dict[j]['W'] += 1
                elif matchup.iloc[stop,idx] > 0 and j in rank_cols:
                    matchup_dict[j]['L'] += 1
                elif matchup.iloc[stop,idx] > 0 :
                    matchup_dict[j]['W'] += 1
                elif matchup.iloc[stop,idx] < 0:
                    matchup_dict[j]['L'] += 1
                else:
                    matchup_dict[j]['T'] += 1
                idx += 1
#GET THE RESULTS OF THE MAIN NON PREDICTION CATEGORIES===========================================================



#GET PREDICTION DICT OUTCOMES============================================================================
for col in prediction_df.columns[1:]:
    prediction_df[col] =  pd.to_numeric(prediction_df[col], errors='coerce')

idx=  [(i,i+1) for i in range(0,prediction_df.shape[0],3)]
# predicted_winners = []
# predicted_winners4 = []
# predicted_winners8 = []
# predicted_winners12 = []
# winners_list = [predicted_winners,predicted_winners4,predicted_winners8,predicted_winners12]

winners_list = [[] for _ in range(len(prediction_df.columns[1:]))]

print(prediction_df.iloc[1,1:])
for (tm1,tm2) in idx:
    count = 0
    temp_diff = prediction_df.iloc[tm1:tm2+1,1:].diff(periods=-1)
    for col in temp_diff.columns:
        if temp_diff.iloc[0,count] > 0:
            winners_list[count].append(prediction_df.iloc[tm1,0])
        elif temp_diff.iloc[0,count] < 0:
            winners_list[count].append(prediction_df.iloc[tm2,0])
        else:
            winners_list[count].append(['TIE'])
        count+=1


# if new_keys[0] not in matchup_dict.keys():
#     matchup_dict['Prediction_0'] = matchup_dict.pop('PREDICTION')


for prediction_list,col_name in zip(winners_list, new_keys[:4]):
    for team in prediction_list:
        postponed = False
        if team not in yest_winners and team not in yest_losers:
            postponed = True
        if not postponed:    
            if team == 'TIE':
                matchup_dict[col_name]['T'] += 1
            elif team in yest_winners:
                matchup_dict[col_name]['W'] += 1
            else:
                matchup_dict[col_name]['L'] += 1
#GET PREDICTION DICT OUTCOMES============================================================================

#add mult and % rows--------------------------------------
# matchup_dict_df= matchup_dict_df.T
# matchup_dict_df['multipliers'] = matchup_dict_df['W']/matchup_dict_df['L']
# matchup_dict_df['%'] = matchup_dict_df['W']/(matchup_dict_df['L']+matchup_dict_df['W'])
# matchup_dict_df= matchup_dict_df.T




#FINAL TOUCHES -----------------MAKE DF, DECIDE IF TEST, AND SEND TO CSV FILE==========================
matchup_dict_df = pd.DataFrame(matchup_dict)
matchup_dict_df= matchup_dict_df.T
matchup_dict_df['multipliers'] = matchup_dict_df['W']/matchup_dict_df['L']
matchup_dict_df['%'] = matchup_dict_df['W']/(matchup_dict_df['L']+matchup_dict_df['W'])
matchup_dict_df= matchup_dict_df.T



print(matchup_dict_df)


#SET THIS TO TRUE IF YOU WANT TO SEND THE RESULTS TO A DIFFERENT FILE FOR TESTING==================
#SET THIS TO TRUE IF YOU WANT TO SEND THE RESULTS TO A DIFFERENT FILE FOR TESTING==================
test = False

if change_file.lower() == 'n':
    test = True
#SET THIS TO TRUE IF YOU WANT TO SEND THE RESULTS TO A DIFFERENT FILE FOR TESTING==================
#SET THIS TO TRUE IF YOU WANT TO SEND THE RESULTS TO A DIFFERENT FILE FOR TESTING==================


version = date.today()
if test:
    filename = f'./test_results_tracker.csv'
    matchup_dict_df.to_csv(filename, index=True)
else:
    filename = f'./results_tracker.csv'
    matchup_dict_df.to_csv(filename, index=True)

    filename = f'./results_tracker{version}.csv'
    matchup_dict_df.to_csv(filename, index=True)