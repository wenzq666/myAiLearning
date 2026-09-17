import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

data = np.random.randn(10,5)
print(type(data))
print(data)


df = pd.DataFrame(data=data,columns=['a','b','c','d','e'])
print(type(df))
print(df.head())
print(df.describe())


df.plot(kind='hist',alpha=0.5)
# plt.show()





























