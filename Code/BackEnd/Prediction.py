import pandas as pd
from fbprophet import Prophet
import pystan

df = pd.read_csv('DB/cameras/192-168-0-100-8080.csv')
df.head()

m = Prophet()
m.params()


