import pandas as pd
from fbprophet import Prophet
import datetime

df = pd.read_csv('DB/dataset.csv')

df['Year'] = df['Time Date'].apply(lambda x: str(x)[-4:])
df['Month'] = df['Time Date'].apply(lambda x: str(x)[-6:-4])
df['Day'] = df['Time Date'].apply(lambda x: str(x)[:-6])
df['ds'] = pd.DatetimeIndex(df['Year']+'-'+df['Month']+'-'+df['Day'])

df = df.loc[(df['Product']==2667437) & (df['Store']=='QLD_CW_ST0203')]
df.drop(['Time Date', 'Product', 'Store', 'Year', 'Month', 'Day'], axis=1, inplace=True)
df.columns = ['y', 'ds']

df.head()

m = Prophet(interval_width=0.95, daily_seasonality=True)
model = m.fit(df)

future = m.make_future_dataframe(periods=100,freq='D')
forecast = m.predict(future)
forecast.head()

plot1 = m.plot(forecast)
plot1.savefig('output1')
plot2 = m.plot_components(forecast)
plot2.savefig('output2')


class Prediction:
    def __init__(self):
        self.data = "LOLOLOL"
        self.predictableTime = "1970-01-01 00:00:00";

    def getPrediction(self, time):
        return self.data



