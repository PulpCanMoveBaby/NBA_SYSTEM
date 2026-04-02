import pandas as pd
from get_main_dataframe import main as get_main_dataframe
from get_multipliers import main as get_mult
from get_clutch import main as get_clutch
from get_hustle import main as get_hustle
from get_shooting import main as get_shooting
from get_win_perc import win_perc_df
from get_todays_matchups import main as get_today_matchups
from get_ngames import main as get_ngames
from minmax import minmax

def main(games, df_dict =None, df_master=None):
    
    #IMPORT DATA FROM OTHER MODS-----------------
    if df_dict is None:
         df_master, df_dict = get_main_dataframe()
    
    master_df = pd.DataFrame()
    clutch_df = get_clutch()
    hustle_df = get_hustle()
    multipliers_df = get_mult(df_dict=df_dict, df_master=df_master)
    multipliers_df_shooting = get_mult('Shooting', df_dict=df_dict, df_master=df_master)
    clutch_df_edited = clutch_df[['Team', 'CLUTCH_SCORE']]
    hustle_df_edited = hustle_df[['Team', 'HUSTLE_SCORE']]

    results_df = pd.read_csv(f'./results_tracker.csv', index_col =0)



    #MAIN LOOP TO CALCULATE MULTIPLE NGAME SCENARIOS------------------------------
    count = 0
    for i in games:
        temp_df = pd.DataFrame()
        scores = get_scores(i, df_dict, multipliers_df)

        #i needs to be a string because Im using an nba_api method that takes n-games as a str
        prescaled_shooting, shooting_df = get_shooting(str(i), multipliers_df_shooting)

        if count == 0:
            #FIRST TIME THROUGH, SET UP THE COLUMNS USED FOR MERGING--------------- 
            scores = pd.merge(scores, win_perc_df, on='Team', how='outer')
            master_df['Team'] = scores['Team']
            master_df['SeasonWin%'] = scores['W_PCT']
            master_df = master_df.sort_values(by='SeasonWin%', ascending=False).reset_index(drop=True)
            master_df['SeasonWinRank'] = list(range(1,len(scores)+1))
            count +=1

        #add columns by game sample--------------------
        temp_df['Team'] = scores['Team']
        temp_df[f'Shooting_{i}'] = shooting_df['SHOOTING_SCORE']
        temp_df[f'Score_{i}'] = scores['Score']
        temp_df = temp_df.sort_values(by=f'Score_{i}', ascending=False).reset_index(drop=True)
        temp_df[f'Rank_{i}'] = list(range(1,len(scores)+1))
        

        #merge the sample to the master df--------------
        master_df = pd.merge(master_df,temp_df, on='Team', how='outer')

    #get season shooting score-----------------------------
    prescaled_shooting, shooting_df = get_shooting('0', multipliers_df_shooting)

    #get lists to use for getting different averages--------------
    scores_avg = [i for i in master_df.columns if i[:5] == 'Score']
    shooting_avg = [i for i in master_df.columns if i[:8] == 'Shooting']
    rank_avg = [i for i in master_df.columns if i[:4] == 'Rank']

    # get averages-----------------------------------------------------------------
    master_df['avg_score'] = master_df[scores_avg].sum(axis=1)/len(scores_avg)
    master_df['avg_shooting'] = master_df[shooting_avg].sum(axis=1)/len(shooting_avg)
    master_df['avg_rank'] = master_df[rank_avg].sum(axis=1)/len(rank_avg)


    #final additions and caluculations------------------------------------------------
    master_df['SeasonPull'] = master_df['avg_rank'] - master_df['SeasonWinRank']
    master_df = pd.merge(master_df, shooting_df[['Team','SHOOTING_SCORE']], on='Team', how='outer')
    master_df.rename(columns={'SHOOTING_SCORE': 'SeasonShooting'}, inplace=True)
    master_df = pd.merge(master_df, hustle_df_edited, on='Team', how='outer')
    master_df = pd.merge(master_df, clutch_df_edited, on='Team', how='outer')
    master_df['ShootingPull'] =  master_df['SeasonShooting'] - master_df['avg_shooting']
    # master_df = pd.merge(master_df, scores_dev[['Team', 'CONSISTENCY']])

    #MINMAX SCALE THE COLUMNS USED FOR SCHS------------------
    minmax_list = ['avg_score','avg_shooting','HUSTLE_SCORE','CLUTCH_SCORE','SeasonPull', 'SeasonShooting', 'Score_8', 'Score_10','ShootingPull']
    for i in minmax_list:
        master_df[i] = minmax(i, master_df)


    #ALLOW THE PERCENTAGE OF COLUMNS USED TO REFLECT REAL WORLD RESULTS===========================
    #THIS IS WHERE COLUMNS THAT NEED TO BE CALCULATED FOR THE MULTIPLIER GO
    #MULTIPLIERS WILL BE CALCULATED FROM THE RESULTS_TRACKER.CSV

    #THIS IS THE PLACE TO ADD OR REMOVE COLUMNS YOU WANT TO FACTOR INTO THE SCHS COLUMN==============================
    get_perc_list = ['SeasonWin%', 'Score_8', 'Score_10', 'SeasonShooting']
    #THIS IS THE PLACE TO ADD OR REMOVE COLUMNS YOU WANT TO FACTOR INTO THE SCHS COLUMN==============================

    perc_list = []
    def get_real_percentages(results_df, name):
        temp =  results_df[name].tolist()
        perc_list.append(temp[0]/(temp[1]))

    #GET MULTIPLIERS FROM THE RESULTS_TRACKER.CSV-----
    for i in get_perc_list:
        get_real_percentages(results_df, i)
    
    #FOR THE CALC SCORE FUNCTION------
    zipped_perc = list(zip(get_perc_list, perc_list))
    

    #CALCULATE THE SCHS COLUMN USING THE COLUMNS OF INTEREST AND THEIR MULTIPLIERS-----------
    master_df['SCHS'] = pd.array([0]*30)
    def calc_score(master_df, zipped_perc):
        for i in zipped_perc:
            if i[0] == 'HUSTLE_SCORE':
                master_df['SCHS'] =  master_df['SCHS'] + master_df[i[0]]*i[1]*0.7
            elif i[0] == 'CLUTCH_SCORE':
                master_df['SCHS'] =  master_df['SCHS'] + master_df[i[0]]*i[1]*0.8
            elif i[0][-4:] == 'Pull':
                master_df['SCHS'] =  master_df['SCHS'] + master_df[i[0]]*i[1]*0.8
            else:
                master_df['SCHS'] =  master_df['SCHS'] + master_df[i[0]]*i[1] 
    calc_score(master_df, zipped_perc)
    master_df = master_df.sort_values(by='SCHS', ascending=False).reset_index(drop=True)
    master_df = master_df.round(2)

    #get csv file-------------------------------------------
    filename = f'./TESTING_RANGES.csv'
    master_df.to_csv(filename, index=False)

    #visualize and run matchup func----------
    print(master_df)
    return master_df


#MAKE THE 2 COLUMN DATAFRAME THAT IS RETURNED TO THE MAIN FUNCTION(Team, Score)=================
def get_scores(num_games, df_dict, multipliers_df):
    #returns dataframe with ngames scaled, abbreviation col named 'Team'
    scaled_matrix = get_ngames(num_games, df_dict)
    scaled_matrix_only_common = pd.DataFrame()
    common_cols = [i for i in multipliers_df.columns if i in scaled_matrix]
    # common_cols = sorted(common_cols)
    scaled_matrix_only_common=scaled_matrix[common_cols]
    mult_vector = multipliers_df.iloc[3,:]
    scores = pd.DataFrame()
    scores['Team'] = scaled_matrix['Team']
    scores["Score"]= scaled_matrix_only_common.dot(mult_vector)
    return scores




#GET MATCHUPS======================================================================================
def get_matchup(matchups, master_df):
    count = 0
    for (tm1, tm2) in matchups:
        print(master_df[master_df['Team'].isin([tm1.upper(), tm2.upper()])])
        print('\n\n')
        filename = f'./today_matchups.csv'
        temp = master_df[master_df['Team'].isin([tm1.upper(), tm2.upper()])]
        if count == 0:
            temp.to_csv(filename, index=False)
            count +=1
        else:
            temp.to_csv(filename, index=False, mode='a')



if __name__ == '__main__':
    # games = [3]
    games = list(range(7,11))
    master_df = main(games)
    matchups = get_today_matchups()
    get_matchup(matchups, master_df)