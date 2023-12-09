import streamlit as st
import pandas as pd
from pandas import Series, DataFrame
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from PIL import Image
import time
# Text/Title
st.write("""
# Stock Market Web Application
*Visually* Show *LIVE* data on Stock and Does *LIVE* Analysis on them  
Created by Akshay Bir
 """
)
#vid_file = open("Stonks.mp4","rb").read()
#st.video(vid_file)
st.sidebar.title(""" *HI!!!*
""")


def data():
    stockname = st.sidebar.text_input("enter name","GOOG")
    st.sidebar.write(stockname)
    #st.sidebar.write("*EXAMPLES*"" if country is other than America"" FOR EXAMPLE - *ETR:BMW*,"" *BSE:RELIANCE*")

    return stockname

def sp():

    choice = st.sidebar.selectbox("SELECT STOCK PERIOD OR ANALSIS",["LIVE STATS","LIVE ANALYSIS"])
    if choice == "LIVE STATS" :
        stockperiod = st.sidebar.selectbox("PERIOD TYPE",["INTRADAY","DAILY","DAILY ADJUSTED","WEEKLY","WEEKLY ADJUSTED","MONTHLY","MONTHLY ADJUSTED"])
        st.write("STOCK TYPE",stockperiod)
    elif choice == "LIVE ANALYSIS":
        stockperiod = st.sidebar.selectbox("ANALYSIS TYPE-",["ANALYSIS BY SMA INTRADAY", "ANALYSIS SMA BY DAILY"])
        st.write("STOCK TYPE", stockperiod)
    return stockperiod

def aintraday(stockname,stockperiod):

    with st.spinner("WAITING ..."):
        time.sleep(18)
    st.success("FINISHED!")



    if stockperiod == "ANALYSIS BY SMA INTRADAY":

        itime = st.sidebar.select_slider("TIME INTERVAL", ["1min", "5min", "15min", "30min", "60min"])
        st.write("""your *TIME INTERVAL* is""", itime)
        st.write(""" # SMA VS CLOSING IF *ORANGE* LINE IS *GREATER* THAN *BLUE* *ITS RIGHT TIME TO INVEST*""")
        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data_ts, meta_data_ts = ts.get_intraday(symbol=stockname, interval=itime, outputsize='full')

        period = 60

        ti = TechIndicators(key='yourapikey', output_format='pandas')
        data_ti, meta_data_ti = ti.get_sma(symbol=stockname, interval=itime,
                                           time_period=period, series_type='close')

        df1 = data_ti
        df2 = data_ts['4. close'].iloc[period - 1::]

        df2.index = df1.index
        #st.text("")
        total_df = pd.concat([df1, df2], axis=1)
        st.line_chart(total_df)
        st.write(total_df)
        st.success(""" 
         *ANALYSIS*
         """)
        st.sidebar.success(""" STOCK DATA!!!""")

    elif stockperiod == "ANALYSIS BY SMA DAILY":

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data_ts, meta_data_ts = ts.get_daily(symbol=stockname, outputsize='full')

        period = 60

        ti = TechIndicators(key='yourapikey', output_format='pandas')
        data_ti, meta_data_ti = ti.get_sma(symbol=stockname,
                                               time_period=period, series_type='close')

        df1 = data_ti
        df2 = data_ts['4. close'].iloc[period - 1::]

        df2.index = df1.index

        total_df = pd.concat([df1, df2], axis=1)
        st.line_chart(total_df)
        st.write(total_df)
        st.success(""" 
                     * ANALYSIS *
                     """)
        st.sidebar.success(""" STOCK DATA!!!""")

    elif stockperiod == "RSI AND SMA":

        itime = st.sidebar.select_slider("TIME INTERVAL", ["1min", "5min", "15min", "30min", "60min"])
        st.write("""your *TIME INTERVAL* is""", itime)
        st.write("""# RSI AND SMA""")
        period = 60
        ti = TechIndicators(key='yourapikey', output_format='pandas')

        data_ti, meta_data_ti = ti.get_rsi(symbol=stockname, interval='1min',
                                           time_period=period, series_type='close')

        data_sma, meta_data_sma = ti.get_sma(symbol=stockname, interval='1min',
                                             time_period=period, series_type='close')

        df1 = data_sma.iloc[1::]
        df2 = data_ti
        df1.index = df2.index

        fig, ax1 = plt.subplots()
        ax1.plot(df1, 'b-')
        ax2 = ax1.twinx()
        ax2.plot(df2, 'r.')

        total_df = pd.concat([df1, df2], axis=1)

        st.area_chart(total_df)
        st.write(total_df)
        st.success(""" 
         **ANALYSIS
         """)
        st.sidebar.success(""" STOCK DATA!!!""")



    elif stockperiod == "INTRADAY":

        itime = st.sidebar.select_slider("TIME INTERVAL", ["1min", "5min", "15min", "30min", "60min"])
        st.write("""your *TIME INTERVAL* is""", itime)

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data_ts = ts.get_intraday(symbol=stockname, interval=itime, outputsize='full')
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *VOlUME* """)
        st.line_chart(data['5. volume'])

    elif stockperiod == "DAILY":

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data = ts.get_daily(symbol=stockname)
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *VOlUME* """)
        st.line_chart(data['5. volume'])

    elif stockperiod == "DAILY ADJUSTED":

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data = ts.get_daily_adjusted(symbol=stockname)
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *ADJUSTED CLOSE* """)
        st.line_chart(data['5. adjusted close'])
        st.write(""" *VOlUME* """)
        st.line_chart(data['6. volume'])

    elif stockperiod == "WEEKLY":

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data = ts.get_weekly(symbol=stockname)
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *VOlUME* """)
        st.line_chart(data['5. volume'])

    elif stockperiod == "WEEKLY ADJUSTED":

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data = ts.get_weekly_adjusted(symbol=stockname)
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *ADJUSTED CLOSE* """)
        st.line_chart(data['5. adjusted close'])
        st.write(""" *VOlUME* """)
        st.line_chart(data['6. volume'])

    elif stockperiod == "MONTHLY" :

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data = ts.get_monthly(symbol=stockname)
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *VOlUME* """)
        st.line_chart(data['5. volume'])

    elif stockperiod == "MONTHLY ADJUSTED" :

        ts = TimeSeries(key='yourapikey', output_format='pandas')
        data, meta_data = ts.get_monthly_adjusted(symbol=stockname)
        st.sidebar.success(""" STOCK DATA!!!""")
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(open=data['1. open'], high=data['2. high'], low=data['3. low'], close=data['4. close']))

        st.plotly_chart(fig)
        st.write(data)
        st.write(""" *Full Chart* """)
        st.line_chart(data)
        st.write(""" *Opening* """)
        st.line_chart(data['1. open'])
        st.write(""" *HIGH* """)
        st.line_chart(data['2. high'])
        st.write(""" *LOW* """)
        st.line_chart(data['3. low'])
        st.write(""" *CLOSING* """)
        st.line_chart(data['4. close'])
        st.write(""" *ADJUSTED CLOSE* """)
        st.line_chart(data['5. adjusted close'])
        st.write(""" *VOLUME* """)
        st.line_chart(data['6. volume'])

stockname = data()
stockperiod = sp()
stockname = aintraday(stockname,stockperiod)
