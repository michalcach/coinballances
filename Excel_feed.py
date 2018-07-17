import pandas as pd


def read_excel_portfolio():

df = pd.read_excel('D:\Dysk Google\VC\Portfolio v15.xlsm',
                   sheet_name='Portfel',
                   skiprows=1,
                   index_col='Data',
                   nrows=270)

print(list(df.columns))

df_portfel = df[['Portfel PLN','Portfel USD']]
print(df_portfel)
