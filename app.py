from flask import Flask, render_template
import sqlite3
import json
import pandas as pd

import pandas_highcharts.core



def read_excel_portfolio():
    df = pd.read_excel('D:\Dysk Google\VC\Portfolio v15.xlsm',
                       sheet_name='Portfel',
                       skiprows=1,
                       index_col='Data',
                       nrows=270)

    # print(list(df.columns))

    df_portfel = df[['Portfel PLN','Portfel USD']]
    df_portfel = df_portfel[:-1]
    # print(df_portfel)
    return df_portfel





app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


@app.route("/data.json")
def data():
    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT 1000*timestamp, measure from measures")
    results = cursor.fetchall()
    print (results)
    return json.dumps(results)

@app.route("/graph")
def graph():
    df = read_excel_portfolio()
    df['Date'] = df.index
    df = df[['Date','Portfel PLN']]
    df_json = df.to_json(orient='values', date_format='epoch')
    print(df_json)
    series = [{"name": 'Label1', "data": df_json}]
    title = {"text": 'My Title'}

    df_returns = df['Portfel PLN']
    print(df_returns.pct_change(7).round(4) * 100)
    returns = { '7 days': df_returns.pct_change(7).iloc[-1].round(4) * 100,
                '8 days': df_returns.pct_change(8).iloc[-1].round(4) * 100,
                '30 days': df_returns.pct_change(30).iloc[-1].round(4) * 100,
                '90 days': df_returns.pct_change(90).iloc[-1].round(4) * 100,
                '120 days': df_returns.pct_change(120).iloc[-1].round(4) * 100
                }

    return render_template('graph.html', title=title, series=series, data=df_json, _dict=returns)



@app.route("/pdh")
def pdh():
    df = pd.read_excel('data\Portfolio.xlsx', index_col='Data')
    df2 = df[['Portfel PLN']]

    portfolioValue = pandas_highcharts.core.serialize(df2,
                                             render_to='my-chart',
                                             output_type='json',
                                             title='Return',)
    hrvDf = df[['Portfolio hrv']]

    hrv = pandas_highcharts.core.serialize(hrvDf,
                                             render_to='my-chart2',
                                             output_type='json',
                                             title='hrv',)


    return render_template('pdh.html', chart=portfolioValue, chart2=hrv)






if __name__ == "__main__":
    app.run(debug=True)