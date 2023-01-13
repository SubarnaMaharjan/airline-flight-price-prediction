import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from feature_eng import data

sns.catplot(y = "Price", x = "Airline", data = data.sort_values("Price", ascending = False), kind="boxen", height = 6, aspect = 3)
plt.show()