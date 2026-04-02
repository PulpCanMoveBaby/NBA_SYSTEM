from get_main_dataframe import main as get_main_df
from get_multipliers import main as get_mult
import matplotlib.pylab as plt
import pandas as pd

df_master, df_dict = get_main_df()
mult_df = get_mult(mode='multipliers')

'''
Example columns for each dict in df_dict===========================================
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
'''

def get_rolling_avg(key1, key2, windows):

    col = df_dict[key1][key2]
    colname = col.name
    print(colname)
    temp_df = pd.DataFrame()
    col = col.reset_index(drop=True)

    plt.figure(figsize=(15,15))
    # col.plot.line()
    for window in windows:
        temp_df[f'mvgavg{window}'] = col.rolling(window=window).mean()
        temp_df[f'mvgavg{window}'].plot(kind='line', title=f'MovingAverage:{key1}_{key2}')
    plt.legend()
    plt.show()

get_rolling_avg('ATL','REB',[10,20])


def get_ema(key1, key2, spans):
    col = df_dict[key1][key2]
    colname = col.name
    print(colname)
    temp_df = pd.DataFrame()
    col = col.reset_index(drop=True)
    plt.figure(figsize=(15,15))
    for span in spans:
        temp_df[f'expavg{span}'] = col.ewm(span=span).mean()
        # col.plot.line()
        temp_df[f'expavg{span}'].plot(kind='line', title=f'ExponentialAverage:{key1}_{key2}')
    plt.legend()
    plt.show()

# get_ema('CHI', 'TOV', [5,10,20])