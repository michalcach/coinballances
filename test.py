import pandas as pd
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
import numpy as np

currencies = ['BTC',
              'ETH',
              'IOT',
              'NEO',
              'OMG',
              'XRP',
              'LTC',
              'WAVES',
              'ARK'
              ]


def timestamp2date(timestamp):
    # function converts a Unix timestamp into Gregorian date
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')


def date2timestamp(date):
    # function coverts Gregorian date in a given format to timestamp
    return datetime.strptime(date_today, '%Y-%m-%d').timestamp()


def fetchCryptoOHLC(fsym, tsym):
    # function fetches a crypto price-series for fsym/tsym and stores
    # it in pandas DataFrame

    cols = ['date', 'timestamp', 'open', 'high', 'low', 'close']
    lst = ['time', 'open', 'high', 'low', 'close']

    timestamp_today = datetime.today().timestamp()
    curr_timestamp = timestamp_today

    for j in range(2):
        df = pd.DataFrame(columns=cols)
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + fsym + "&tsym=" + tsym + "&toTs=" + str(
            int(curr_timestamp)) + "&limit=2000"
        # print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dic = json.loads(soup.prettify())
        try:
            for i in range(1, 2001):
                tmp = []
                for e in enumerate(lst):
                    x = e[0]
                    y = dic['Data'][i][e[1]]
                    if (x == 0):
                        tmp.append(str(timestamp2date(y)))
                    tmp.append(y)
                if (np.sum(tmp[-4::]) > 0):
                    df.loc[len(df)] = np.array(tmp)
            df.index = pd.to_datetime(df.date)
            df.drop('date', axis=1, inplace=True)
            curr_timestamp = int(df.ix[0][0])
        except:
            print('detka')
        if (j == 0):
            df0 = df.copy()
        else:
            data = pd.concat([df, df0], axis=0)
    return data


tsym = "USD"

print('Downloading data')
for cur in currencies:
    # print('checking: {}'.format(cur))
    df_temp = fetchCryptoOHLC(cur, tsym)
    df_temp = df_temp[['close']].astype('float64')
    # print(df_temp.dtypes)
    # df_temp = pd.to_numeric(df_temp)
    df_temp = df_temp.rename(columns={'close': cur})
    # print(df_temp)
    if cur == 'BTC':
        df = df_temp
    else:
        df = df.join(df_temp)

df_temp = fetchCryptoOHLC('BTC', 'PLN')
df_temp = df_temp[['close']].astype('float64')
df_temp = df_temp.rename(columns={'close': 'BTCPLN'})
df = df.join(df_temp)

print('Download completed')

from shutil import copyfile

file = 'D:\Dysk Google\VC\Portfolio v15.xlsm'
file_backup = 'D:\Dysk Google\VC\Portfolio v15_' + datetime.now().strftime("%Y-%m-%d_%H%M") + '.xlsm'

copyfile(file, file_backup)

from openpyxl import load_workbook

dfP = df[(df.index >= "2017-07-31")]

book = load_workbook(file, keep_vba=True)

writer = pd.ExcelWriter(file, engine='openpyxl')

writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

dfP.to_excel(writer, "Prices2")

writer.save()

print('Saving to Excel Completed')

# import os

# os.startfile('D:\Dysk Google\VC\Portfolio v15.xlsm')

