import pandas as pd

def minmax(col, df):
    min = df[col].min()
    max = df[col].max()
    return (df[col]-min)/(max-min)
