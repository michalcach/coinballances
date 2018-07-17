import pandas as pd


df = pd.read_excel('data\Portfolio.xlsx', index_col='Data')

print(df['Portfel PLN'])
print(df.dtypes)
# print(list(df.columns))
# print(df.shape)
# print(df.loc[:,['Portfel PLN']])