import pandas as pd
from fbprophet import Prophet
import datetime
import os
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING)

class suppress_stdout_stderr(object):
    def __init__(self):
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

class Prediction:
    def __init__(self):
        self.predictableTime = "1970-01-01 00:00:00"
        self.df = pd.read_csv('DB/cameras/192-168-0-176-8080.csv')
        self.df['ds'] = pd.DatetimeIndex(self.df['time'])
        self.periodNum = 0
        self.stringList = ["0-6 éves kor: ", "6-12 éves kor: ", "12-18 éves kor: ", "18-26 éves kor: ", "26-36 éves kor: ",
                           "36-48 éves kor: ", "48-60 éves kor: ", "60-100 éves kor: ", "Nő: ", "Férfi: "]

    def getPrediction(self, time):
        self.predictableTime = time
        self.countPeriodNum()
        return self.predictableTime + "\n" + self.predict()

    def countPeriodNum(self):
        refDate = str((pd.DatetimeIndex(self.df['time']).values)[len(self.df.index) - 1])
        refDate = refDate[:19]
        refDate = refDate[:10] + " " + refDate[-8:]

        refDateObject =  datetime.datetime.strptime(refDate, '%Y-%m-%d %H:%M:%S')
        predDateObject = datetime.datetime.strptime(self.predictableTime, '%Y-%m-%d %H:%M:%S')

        diff = predDateObject - refDateObject
        hourDiff = diff.days * 24 + diff.seconds / (3600)
        self.periodNum = int(hourDiff / 2)

    def getValue(self, x, id):
        x = x.replace('[', '')
        x = x.replace(']', '')
        x = x.split(', ')
        return int(x[id])

    def predict(self):
        information = ""
        dataList = []
        ageSum = 0
        genderSum = 0

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
            future = m.make_future_dataframe(periods=self.periodNum, freq='2H', include_history=False)
            forecast = m.predict(future)
            forecast.head()

            personPred = forecast[['yhat']].values[self.periodNum - 1][0]
            if i < 8:
                ageSum += personPred
            else:
                genderSum += personPred
            dataList.append(personPred)

        for i in range(8):
            information += self.stringList[i] + str(round((dataList[i] / ageSum) * 100, 2)) + "% \n"
        information += "\n"
        for i in range(8, 10):
            information += self.stringList[i] + str(round((dataList[i] / genderSum) * 100, 2)) + "% \n"

        return information

predict = Prediction()
print(predict.getPrediction('2021-04-02 08:00:00'))

