import pandas as pd

df = pd.read_csv('songlist.csv')
print(df.nunique())
print(df['ARTIST CLEAN'].unique())
