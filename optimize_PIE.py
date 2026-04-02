from get_multipliers import main as get_mult
from get_main_dataframe import main as get_dataframe
from get_win_perc import win_perc_df
from get_ngames import main as get_ngames
from minmax import minmax
import pandas as pd

#only run if df_dict has not been created
if 'df_dict' not in dir():
    df_master, df_dict = get_dataframe()
multipliers_df = get_mult(df_dict=df_dict, df_master=df_master)
    # df_master, df_dict = get_dataframe()

#get common
x = set(multipliers_df.columns)
y = set(df_dict['CHI'].columns)
common_cols =  sorted(x.intersection(y))

#set three mults to 0 ====
new_labels = ['W', 'L', 'T', 'mult']
multipliers_df.index = new_labels
multipliers_df.loc['mult','NET_RATING'] = 0
multipliers_df.loc['mult','OPP_PTS'] = 0
multipliers_df.loc['mult','PIE'] = 0


#make a list of last n games--------------------------------
ngames_list = []
for i in range(6,11):
    ngames_dict = get_ngames(i,df_dict)
    ngames_dict = ngames_dict.sort_values(by='Team').reset_index(drop=True)
    ngames_list.append(ngames_dict)
team_array = pd.array(ngames_dict['Team'])
win_perc_df = win_perc_df.sort_values(by='Team').reset_index(drop=True)



data = []
def get_score(multipliers_df, ngames_list, common_cols, win_perc_df, end_test = False):
    temp_df = pd.DataFrame()
    temp_scores = pd.DataFrame()
    dot_array = pd.DataFrame(multipliers_df.loc['mult', :])
    count = 5
    for ngames in ngames_list:
        count +=1
        for col in multipliers_df.columns:
            if col in common_cols:
                temp_df[col] = ngames[col]
        temp_scores[f'score_{count}'] = temp_df.dot(dot_array)
        temp_scores[f'score_{count}'] = minmax(f'score_{count}',temp_scores)
    
    temp_scores['avg_score'] = temp_scores.mean(axis=1)

    temp_scores['Team'] = ngames_dict['Team']
    error_df = pd.merge(win_perc_df, temp_scores, on='Team', how='outer')
    error_df['W_PCT'] = minmax('W_PCT', error_df)
    error_df['error'] = (error_df['W_PCT'] - error_df['avg_score'])
    error_df['sq_error'] = error_df['error']*error_df['error']
    sum_sq_error = sum(error_df['sq_error'])
    data.append([multipliers_df.loc['mult','NET_RATING'],
                multipliers_df.loc['mult','OPP_PTS'],
                multipliers_df.loc['mult','PIE'],
                sum_sq_error])


#CHANGE THIS TO CALUCULATE LOCAL WITH OPP_PTS=================
no_opp_pts = True
#==============================================================


#TRUE TO TURN ON THE OPTIMIZER BETWEEN 700 and 1000===========
get_optimum = True
#==============================================================


if get_optimum:
    #run a quick scan to see if adding in opp pts helps to minimize the error
    if no_opp_pts == False:
        batch_i = range(0,1100, 100)
        batch_k = range(0,1100, 100)
        batch_j = range(0,1100, 100)
    else:
        #batch_j is not used here, just a placeholder to keep the same format as the other loop
        batch_i = range(700,1010, 10)
        batch_k = range(700,1010, 10)
        batch_j = range(700,1010, 10)

    for i in batch_i:
        multipliers_df.loc['mult','NET_RATING'] = i
        for k in batch_k:
            multipliers_df.loc['mult','PIE'] = k
            if no_opp_pts:
                j = 0
                multipliers_df.loc['mult','OPP_PTS'] = j
                if data:
                    print(f'Starting --> {i} {j} {k} {data[-1][3]}')
                else:
                    print(f'Starting --> {i} {j} {k}')
                get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
            else:
                for j in batch_j:
                    multipliers_df.loc['mult','OPP_PTS'] = j
                    if data:
                        print(f'Starting --> {i} {j} {k} {data[-1][3]}')
                    else:
                        print(f'Starting --> {i} {j} {k}')
                    get_score(multipliers_df, ngames_list, common_cols, win_perc_df)


    data = sorted(data, key=lambda x: x[3])
    # batch_i = range(int(data[0][0]-30), int(data[0][0]+30))
    # batch_k = range(int(data[0][2]-30), int(data[0][2]+30))
    # if no_opp_pts == True:
    #     for i in batch_i:
    #         multipliers_df.loc['mult','NET_RATING'] = i
    #         for k in batch_k:
    #             multipliers_df.loc['mult','PIE'] = k
    #             if no_opp_pts:
    #                 j = 0
    #                 multipliers_df.loc['mult','OPP_PTS'] = j
    #                 print(f'Starting --> {i} {j} {k} {data[-1][3]}')
    #                 get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
    #             else:
    #                 for j in batch_j:
    #                     multipliers_df.loc['mult','OPP_PTS'] = j
    #                     print(f'Starting --> {i} {j} {k} {data[-1][3]}')
    #                     get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
    #     data = sorted(data, key=lambda x: x[3])
    # main_df = pd.DataFrame(data)
    # filename = '/home/k/betting_code/edited_code/optimize_pie3.csv'
    # main_df.to_csv(filename, index=False)


    multipliers_df.loc['mult','NET_RATING'] = int(data[0][0])
    multipliers_df.loc['mult','PIE'] = int(data[0][2])
    

    count_a = 0
    count_b = 0
    if no_opp_pts:
        while True:
            stat = 'NET_RATING' if int(data[0][0]) > int(data[0][2]) else 'PIE'
            other_stat = 'NET_RATING' if stat == 'PIE' else 'PIE'
            if count_a == 1000:
                if multipliers_df.loc['mult',other_stat] == 0:
                    break
                multipliers_df.loc['mult',other_stat] -= 1
                print(data[0])
                get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
                if float(data[-1][3]) < float(data[0][3]):
                    count_b +=1
                    data[0] = data[-1]
                else:
                    print(data[0], data[-1]) 
                    break 
            else:
                multipliers_df.loc['mult',stat] += 1
                get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
                if float(data[-1][3]) < float(data[0][3]):
                    count_a +=1
                    data[0] = data[-1]
                    print(data[0])
                    # multipliers_df.loc['mult',stat] += 1
                    get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
                else:
                    print(data[0], data[-1]) 
                    break


    # count_a = 0
    # while True:
    #     if count_a == 200:
    #         break
    #     stat = 'NET_RATING' if int(data[0][0]) > int(data[0][2]) else 'PIE'
    #     multipliers_df.loc['mult',stat] += 1
    #     get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
    #     if float(data[-1][3]) < float(data[0][3]):
    #         count +=1
    #         data[0] = data[-1]
    #         print('here')
    #         # multipliers_df.loc['mult',stat] += 1
    #         get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
    #     else:
    #         print(data[0], data[-1]) 
    #         break

    # data = sorted(data, key=lambda x: x[3])
    # main_df = pd.DataFrame(data)
    # filename = '/home/k/betting_code/edited_code/optimize_pie2.csv'
    # main_df.to_csv(filename, index=False)
    # new_min = data[0][3]

    data = sorted(data, key=lambda x: x[3])
    main_df = pd.DataFrame(data)
    filename = f'./optimize_pie.csv'
    main_df.to_csv(filename, index=False)
    print(data[:10])



#TURN ON THE LOCAL MINIMA LOOP=================================
get_local = False
#==============================================================


if get_local == True:
    local_minima = []
    data = []
    for x in range(7):
        batch_i = range(x*100+100,x*100+300, 10)
        batch_k = range(x*100+100,x*100+300, 10)
        batch_j = range(x*100+100,x*100+300, 10)
        for i in batch_i:
            multipliers_df.loc['mult','NET_RATING'] = i
            for k in batch_k:
                multipliers_df.loc['mult','PIE'] = k
                if no_opp_pts:
                    j = 0
                    multipliers_df.loc['mult','OPP_PTS'] = j
                    print(f'Starting --> {i} {j} {k}')
                    get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
                else:
                    for j in batch_j:
                        multipliers_df.loc['mult','OPP_PTS'] = j
                        print(f'Starting --> {i} {j} {k}')
                        get_score(multipliers_df, ngames_list, common_cols, win_perc_df)
        data = sorted(data, key=lambda x: x[3])
        local_minima.append([x*100+100,x*100+200,data[0]])

        locals = pd.DataFrame(local_minima)
        filename = f'./local_minima.csv'
        locals.to_csv(filename, index=False)
        print(local_minima)