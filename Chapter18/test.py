import pandas as pd 
import matplotlib.pyplot as plt 
df = pd.read_excel(r'//Users/xuyuanwu/Desktop/Python/Quant/Chapter18/test1.xlsx')
df.head()
plt.plot(df.日期,df.值2)
plt.show()