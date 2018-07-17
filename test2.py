import pandas as pd


df = pd.read_hdf('balances.h5', 'balances')

print(df.to_string())

print(df.dtypes)

df_day = df.set_index('TimeStamp').groupby([pd.TimeGrouper(freq='10MIN'), 'CURRENCY', 'Source','USD','BTC']).last()
print(df_day.to_string())
df_day = df_day.groupby(['TimeStamp','CURRENCY']).sum()
print(df_day.to_string())
