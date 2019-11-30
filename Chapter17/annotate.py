import numpy as np
import matplotlib.pyplot as plt

x=np.arange(-10,11,1)
y=x*x

plt.plot(x,y)
plt.annotate(u"This is a graph",xy=(1,2),xytext = (1,50),arrowprops=dict(facecolor='r',headlength=10,headwidth=30,width=20))

plt.show()
