import matplotlib.pyplot as plt
import numpy as np


import pandas as pd

df = pd.read_csv('logBom/1100-1900_nobec_vertical_flowmeter.txt', header = None)
a= df.to_numpy()
#timeStamp = a[:,0]
Q = a[:,0]
pulse = a[:,1]
#print Q
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()

#print df
ax1.plot( Q, marker='',color='skyblue', linewidth=1)
ax2.plot( pulse, marker='', color='olive', linewidth=1)
#plt.plot( 2, 3, data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
plt.legend()
plt.show()
while True:
	pass