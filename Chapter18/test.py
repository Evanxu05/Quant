import numpy as np

import matplotlib.pyplot as plt

import matplotlib.dates as mdates

import matplotlib.gridspec as gridspec #分割子图

import mpl_finance as mpf

import pandas as pd

import pandas_datareader.data as web

import datetime

import talib

import csv,os,codecs

import tushare as ts

plt.rcParams['font.sans-serif']=['Arial Unicode MS'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def plot_trade(stock_df):

    if os.path.isfile(r'/Users/xuyuanwu/Desktop/Python/Quant/Chapter18/ZDWX600797.csv'):                		
        f=codecs.open(r'/Users/xuyuanwu/Desktop/Python/Quant/Chapter18/ZDWX600797.csv', 'rb', 'gb2312')
    #GB2312编码——>unicode

        reader = csv.DictReader(f)

        for row in reader:

            buy_date = row["买入时间"]

            sell_date = row["卖出时间"]

            hands_num =  row["股数"]

            start = stock_df.index.get_loc(buy_date)#'2017-01-16'

            end = stock_df.index.get_loc(sell_date)#'2017-03-16'            

            if stock_df.Close[end] < stock_df.Close[start]:#赔钱显示绿色
               				
                plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='green', alpha=0.38)
                is_win = False

            else: #赚钱显示红色
                plt.fill_between(stock_df.index[start:end], 0, stock_df.Close[start:end], color='red', alpha=0.38)
                is_win = True

            plt.annotate('获利'+hands_num+u'手' if is_win else '亏损\n'+hands_num+u'手',xy=(sell_date,stock_df.Close.asof(sell_date)),xytext=(sell_date,stock_df.Close.asof(sell_date)+4),arrowprops=dict(facecolor='yellow',shrink=0.1),horizontalalignment='left',verticalalignment='top')

            print(buy_date,sell_date)

        f.close()

        plt.plot(stock_df.index,stock_df.Close,color='r')

        """整个时间序列填充为底色blue 透明度alpha小于后标注区间颜色"""    

        plt.fill_between(stock_df.index,0,stock_df.Close,color='blue',alpha=.08)

        plt.xlabel('time')

        plt.ylabel('close')

        plt.title(u'浙大网新')

        plt.grid(True)

        plt.ylim(np.min(stock_df.Close)-5,np.max(stock_df.Close)+5)#设置Y轴范围

        plt.legend(['Close'],loc='best')

        plt.show()

stock = web.DataReader("600797.SS", "yahoo", datetime.datetime(2018,1,1), datetime.datetime(2018,12,31))

plot_trade(stock)