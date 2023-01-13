import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import feature_eng as fe

data = pd.read_excel(r'/home/vylericd3vil/Minor-project/Dataset/Data_Train.xlsx')

sns.catplot(y = "Price", x = "Airline", data = data.sort_values("Price", ascending = False), kind="boxen", height = 6, aspect = 3)
plt.show()