#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec#分割子图
import mpl_finance as mpf #替换 import matplotlib.finance as mpf
import pandas as pd
import pandas_datareader.data as web
import datetime
from datetime import timedelta
import talib
import tushare as ts
ts.set_token('fd5caf31a54962a7509e7d4d7972d235dbbc4f0c583003d0ef22d2cf')
pro = ts.pro_api()

plt.rcParams['font.sans-serif']=['Arial Unicode MS'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#股票基础信息
stock_code = "000016.SH"#设置股票代码
End_date = datetime.date.today()
Start_date = End_date-timedelta(40)

df_stockload = ts.pro_bar(ts_code=stock_code, asset='I', start_date=Start_date.strftime('%Y%m%d'), end_date=End_date.strftime('%Y%m%d'),freq='15min',ma=[8, 16, 48,96])
df_stockload = df_stockload.sort_index(ascending=False)#降序排序
#df_stockload = df_stockload.sort_index()#升序排序

#python3.7打印
print (df_stockload.head())#查看前几行 
print (df_stockload.columns)#查看列名
print (df_stockload.index)#查看索引
print (df_stockload.describe())#查看各列数据描述性统计



fig = plt.figure(figsize=(14,8), dpi=100,facecolor="white")#创建fig对象
#fig.subplots_adjust(left=0.09,bottom=0.20, right=0.94,top=0.90, wspace=0.2, hspace=0)
#graph_KAV = fig.add_subplot(1,1,1)#创建子图

gs = gridspec.GridSpec(5, 1, left=0.05, bottom=0.2, right=0.96, top=0.96, wspace=None, hspace=0, height_ratios=[3.5,1,1,1,1])
graph_KAV = fig.add_subplot(gs[0,:])
graph_VOL = fig.add_subplot(gs[1,:])
graph_MACD = fig.add_subplot(gs[2,:])
graph_MACD1 = fig.add_subplot(gs[3,:])
graph_MACD2 = fig.add_subplot(gs[4,:])

""" 绘制K线图 """
#方法1
ohlc = []
ohlc = list(zip(np.arange(0,len(df_stockload.index)),df_stockload.open,df_stockload.close,df_stockload.high,df_stockload.low))#使用zip方法生成数据列表 
mpf.candlestick_ochl(graph_KAV, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0)#绘制K线走势
#方法2
#mpf.candlestick2_ochl(graph_KAV, df_stockload.Open,df_stockload.Close,df_stockload.High,df_stockload.Low, width=0.5, colorup='r', colordown='g')#绘制K线走势
""" 绘制K线图 """

""" 绘制移动平均线图 """


numt = np.arange(0, len(df_stockload.index))

#绘制均线走势    
graph_KAV.plot(numt, df_stockload['ma8'],'black', label='M8',lw=1.0)
graph_KAV.plot(numt, df_stockload['ma16'],'green',label='M16', lw=1.0)
graph_KAV.plot(numt, df_stockload['ma48'],'blue',label='M48', lw=1.0)
graph_KAV.plot(numt, df_stockload['ma96'],'yellow',label='M96', lw=1.0)
graph_KAV.legend(loc='best')

""" 绘制移动平均线图 """

#fig.suptitle('600797 浙大网新', fontsize = 14, fontweight='bold')
graph_KAV.set_title(stock_code + u"15分钟线")
#graph_KAV.set_xlabel("日期")
graph_KAV.set_ylabel(u"价格")
graph_KAV.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_KAV.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
graph_KAV.grid(True,color='k')
graph_KAV.set_xticklabels([df_stockload.trade_time[index] for index in graph_KAV.get_xticks()])#标签设置为日期


""" 绘制成交量图 """

graph_VOL.bar(numt, df_stockload.vol,color=['g' if df_stockload.open[x] > df_stockload.close[x] else 'r' for x in range(0,len(df_stockload.index))])

graph_VOL.set_ylabel(u"成交量")
#graph_VOL.set_xlabel("日期")
graph_VOL.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_VOL.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
#graph_VOL.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_VOL.get_xticks()])#标签设置为日期

""" 绘制成交量图 """


''' 绘制MACD '''   
         
macd_dif, macd_dea, macd_bar = talib.MACD(df_stockload['close'].values, fastperiod=16, slowperiod=32, signalperiod=12)
graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dif, 'red', label='macd dif') #dif    
graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dea, 'blue', label='macd dea') #dea 
#绘制BAR>0 柱状图
bar_red = np.where(macd_bar>0, 2*macd_bar, 0)
#绘制BAR<0 柱状图
bar_green = np.where(macd_bar<0, 2*macd_bar, 0)        
graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_red, facecolor='red')
graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_green, facecolor='green')
graph_MACD.legend(loc='best',shadow=True, fontsize ='10')

graph_MACD.set_ylabel(u"MACD")
#graph_MACD.set_xlabel("日期")
graph_MACD.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_MACD.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
#graph_MACD.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_MACD.get_xticks()])#标签设置为日期

''' 绘制MACD ''' 

''' 绘制MACD1 '''   
         
macd_dif1, macd_dea1, macd_bar1 = talib.MACD(df_stockload['close'].values, fastperiod=8, slowperiod=16, signalperiod=6)
graph_MACD1.plot(np.arange(0, len(df_stockload.index)), macd_dif1, 'red', label='macd dif1') #dif    
graph_MACD1.plot(np.arange(0, len(df_stockload.index)), macd_dea1, 'blue', label='macd dea1') #dea 
#绘制BAR>0 柱状图
bar_red1 = np.where(macd_bar1>0, 2*macd_bar1, 0)
#绘制BAR<0 柱状图
bar_green1 = np.where(macd_bar1<0, 2*macd_bar1, 0) 
graph_MACD1.bar(np.arange(0, len(df_stockload.index)), bar_green1, facecolor='green')
graph_MACD1.legend(loc='best',shadow=True, fontsize ='10')

graph_MACD1.set_ylabel(u"MACD")
#graph_MACD.set_xlabel("日期")
graph_MACD1.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_MACD1.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
#graph_MACD.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_MACD.get_xticks()])#标签设置为日期

''' 绘制MACD1 ''' 

''' 绘制MACD2 '''   
         
macd_dif2, macd_dea2, macd_bar2 = talib.MACD(df_stockload['close'].values, fastperiod=48, slowperiod=96, signalperiod=36)
graph_MACD2.plot(np.arange(0, len(df_stockload.index)), macd_dif2, 'red', label='macd dif2') #dif    
graph_MACD2.plot(np.arange(0, len(df_stockload.index)), macd_dea2, 'blue', label='macd dea2') #dea 
#绘制BAR>0 柱状图
bar_red2 = np.where(macd_bar2>0, 2*macd_bar2, 0)
#绘制BAR<0 柱状图
bar_green2 = np.where(macd_bar2<0, 2*macd_bar2, 0)        
graph_MACD2.bar(np.arange(0, len(df_stockload.index)), bar_red2, facecolor='red')
graph_MACD2.bar(np.arange(0, len(df_stockload.index)), bar_green2, facecolor='green')
graph_MACD2.legend(loc='best',shadow=True, fontsize ='10')

graph_MACD2.set_ylabel(u"MACD")
#graph_MACD.set_xlabel("日期")
graph_MACD2.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_MACD2.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
#graph_MACD.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_MACD.get_xticks()])#标签设置为日期

''' 绘制MACD2 ''' 




#X-轴每个ticker标签都向右倾斜45度 

for label in graph_KAV.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)

for label in graph_VOL.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)

for label in graph_MACD.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)

for label in graph_MACD1.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)		


for label in graph_MACD2.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)

plt.show()
