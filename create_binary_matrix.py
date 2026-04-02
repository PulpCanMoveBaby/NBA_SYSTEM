#! /home/k/nba/bin/python3

import pandas as pd
import sys

if len(sys.argv) > 1:
    value = int(sys.argv[1])
else:
    value = 2

def create_matrix(bits):
    matrix = []
    total = (2**bits)-1
    for i in range(total+1):
        target = i
        entry = []
        for bit in reversed(list(range(bits))):
            if target >=2**bit:
                entry.append(1)
                target = target%2**bit
            else:
                entry.append(0)
        matrix.append(entry)
    return matrix



matrix = create_matrix(value)
binary_df = pd.DataFrame(matrix)
filename = f'./binary_matrix_{value}.csv'
binary_df.to_csv(filename, index = False)
