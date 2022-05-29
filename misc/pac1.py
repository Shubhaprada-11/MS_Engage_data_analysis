import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("cars_engage_2022.csv")
#df = pd.read_csv("../../Downloads/biostats.csv")
df.info(verbose=False, memory_usage="deep")
print(df.shape)
#print(df.head)
print(df.describe())
print(df.groupby('Name').describe())
df.plot.bar()
