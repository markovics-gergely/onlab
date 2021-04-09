import pandas as pd
from fbprophet import Prophet
import datetime
import os
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING)



'''df['Year'] = df['Time Date'].apply(lambda x: str(x)[-4:])
df['Month'] = df['Time Date'].apply(lambda x: str(x)[-6:-4])
df['Day'] = df['Time Date'].apply(lambda x: str(x)[:-6])'''

'''plot1 = m.plot(forecast)
plot1.savefig('output1')
plot2 = m.plot_components(forecast)
plot2.savefig('output2')'''

class suppress_stdout_stderr(object):

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])


class Prediction:
    def __init__(self):
        self.data = "LOLOLOL"
        self.predictableTime = "1970-01-01 00:00:00"
        self.df = pd.read_csv('DB/cameras/192-168-0-176-8080.csv')
        self.df['ds'] = pd.DatetimeIndex(self.df['time'])

    def getPrediction(self, time):
        self.predict()
        return self.data

    def getValue(self, x, id):
        x = x.replace('[', '')
        x = x.replace(']', '')
        x = x.split(', ')
        return int(x[id])

    def predict(self):
        for i in range(10):
            predictdf = self.df.copy()
            if i < 8:
                predictdf['y'] = self.df['age'].apply(lambda x: self.getValue(x, i))
            else:
                predictdf['y'] = self.df['gender'].apply(lambda x: self.getValue(x, i - 8))
            predictdf.drop(['time', 'gender', 'age'], axis=1, inplace=True)

            m = Prophet(interval_width=0.95, daily_seasonality=True, growth='linear')
            with suppress_stdout_stderr():
                model = m.fit(predictdf)
            future = m.make_future_dataframe(periods=2, freq='2H', include_history=False)
            forecast = m.predict(future)
            forecast.head()
            print(predictdf.tail())
            #forecast.to_csv("asd.csv", index=False)
            print(forecast[['ds', 'yhat']].tail())

predict = Prediction()
predict.predict()

