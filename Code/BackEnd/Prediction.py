import pandas as pd
from fbprophet import Prophet
import datetime
import os
import sys
import time

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
        self.ip = "0-0-0-0-0"
        self.periodNum = 0
        self.stringList = ["0-6 éves kor: ", "6-12 éves kor: ", "12-18 éves kor: ", "18-26 éves kor: ", "26-36 éves kor: ",
                           "36-48 éves kor: ", "48-60 éves kor: ", "60-100 éves kor: ", "Nő: ", "Férfi: "]

    def loadCamera(self):
        self.df = pd.read_csv('DB/cameras/' + self.ip + '.csv')
        self.df['ds'] = pd.DatetimeIndex(self.df['time'])

    def loadHolidays(self):
        nationalHoliday = pd.DataFrame({
            'holiday': 'nationalHoliday',
            'ds': pd.to_datetime(['2000-03-15', '2000-05-01', '2000-08-20', '2000-10-23']),
            'lower_window': 0,
            'upper_window': 1,
        })
        otherHoliday = pd.DataFrame({
            'holiday': 'otherHoliday',
            'ds': pd.to_datetime(['2000-12-24', '2000-12-25', '2000-12-26']),
            'lower_window': 0,
            'upper_window': 1,
        })
        self.holidays = pd.concat((nationalHoliday, otherHoliday))


    def getPrediction(self, time, ip):
        self.ip = ip
        self.loadCamera()
        self.loadHolidays()
        self.predictableTime = time
        self.countPeriodNum()

        return self.predictableTime + "\n\n" + self.predict()

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

    def progressBar(self, i) :
        sys.stdout.write("\r{2}% <{0}/{1}>\r".format("="*(i + 1),"-"*(9 - i), (i + 1) * 10))
        sys.stdout.flush()

    def predict(self):
        information = ""
        dataList = []
        ageSum = 0
        genderSum = 0

        self.progressBar(-1)
        for i in range(10):
            predictdf = self.df.copy()
            if i < 8:
                predictdf['y'] = self.df['age'].apply(lambda x: self.getValue(x, i))
            else:
                predictdf['y'] = self.df['gender'].apply(lambda x: self.getValue(x, i - 8))
            predictdf.drop(['time', 'gender', 'age'], axis=1, inplace=True)

            m = Prophet(interval_width=0.95, daily_seasonality=True, weekly_seasonality=False, yearly_seasonality=False, growth='linear', holidays=self.holidays)
            m.add_country_holidays(country_name='HU')

            with suppress_stdout_stderr():
                m.fit(predictdf)
            future = m.make_future_dataframe(periods=self.periodNum, freq='2H', include_history=False)
            forecast = m.predict(future)
            forecast.head()

            #m.plot(forecast)
            #m.plot_components(forecast)

            personPred = forecast[['yhat']].values[self.periodNum - 1][0]
            if i < 8:
                ageSum += personPred
            else:
                genderSum += personPred
            dataList.append(personPred)

            self.progressBar(i)

        for i in range(8):
            information += self.stringList[i] + str(round((dataList[i] / ageSum) * 100, 2)) + "% -> " + str(round(dataList[i], 2)) + "\n"
        information += "\n"
        for i in range(8, 10):
            information += self.stringList[i] + str(round((dataList[i] / genderSum) * 100, 2)) + "% -> " + str(round(dataList[i], 2)) + "\n"

        return information

#predict = Prediction()
#print(predict.getPrediction('2021-04-02 08:00:00', '192-168-0-176-8080'))

