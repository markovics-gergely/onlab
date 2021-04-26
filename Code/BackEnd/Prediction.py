import pandas as pd
from fbprophet import Prophet
import datetime
import os
import sys
import random
import holidays as holidays
from matplotlib import pyplot as plt
from fbprophet.plot import plot_forecast_component, plot_yearly, plot_weekly
import time
import threading

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
        self.stringList = ["0-6 years old: ", "6-12 years old: ", "12-18 years old: ", "18-26 years old: ", "26-36 years old: ",
                           "36-48 years old: ", "48-60 years old: ", "60-100 years old: ", "Women: ", "Men: "]

        self.figures = []
        self.axises = []
        
        self.models = []
        self.forecasts = []

    def loadCamera(self):
        self.df = pd.read_csv('DB/cameras/' + self.ip + '.csv')
        self.df['ds'] = pd.DatetimeIndex(self.df['time'])

    def loadHolidays(self):
        df = pd.read_csv('DB/holidays.csv')
        self.holidays = df

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
        sys.stdout.write("\r{2}% <{0}|{1}>\r".format("="*(i + 1),"-"*(9 - i), (i + 1) * 10))
        sys.stdout.flush()

    def predict(self):
        information = ""
        dataList = []
        ageSum = 0
        genderSum = 0

        self.models = []
        self.forecasts = []
        self.progressBar(-1)

        self.figures = [plt.figure(),plt.figure(),
                        plt.figure(),plt.figure(),
                        plt.figure(),plt.figure()]
        for i in range(6) :
            self.axises.append(self.figures[i].add_subplot(1,1,1))


        for i in range(10):
            predictdf = self.df.copy()
            if i < 8:
                predictdf['y'] = self.df['age'].apply(lambda x: self.getValue(x, i))
            else:
                predictdf['y'] = self.df['gender'].apply(lambda x: self.getValue(x, i - 8))
            predictdf.drop(['time', 'gender', 'age'], axis=1, inplace=True)

            m = Prophet(interval_width=0.95, daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True, growth='linear', holidays=self.holidays)
            m.add_seasonality(name="monthly", period=30.5*12, fourier_order=8)

            with suppress_stdout_stderr():
                m.fit(predictdf)
            future = m.make_future_dataframe(periods=self.periodNum, freq='2H', include_history=False)
            future['floor'] = 0
            forecast = m.predict(future)
            forecast.head()

            self.models.append(m)
            self.forecasts.append(forecast)

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

    def processPlot(self) :
        i = 0
        try:
            while(i != 10) :
                if i < 8 :
                    plot_forecast_component(m=self.models[i], name='trend', ax=self.axises[0], fcst=self.forecasts[i])
                    plot_yearly(m=self.models[i], ax=self.axises[1])
                    plot_weekly(m=self.models[i], ax=self.axises[2])
                    self.axises[0].get_lines()[i].set_color('C' + str(i))
                    self.axises[1].get_lines()[i].set_color('C' + str(i))
                    self.axises[2].get_lines()[i].set_color('C' + str(i))
                else :
                    plot_forecast_component(m=self.models[i], name='trend', ax=self.axises[3], fcst=self.forecasts[i])
                    plot_yearly(m=self.models[i], ax=self.axises[4])
                    plot_weekly(m=self.models[i], ax=self.axises[5])
                    self.axises[3].get_lines()[i - 8].set_color('C' + str(i))
                    self.axises[4].get_lines()[i - 8].set_color('C' + str(i))
                    self.axises[5].get_lines()[i - 8].set_color('C' + str(i))
                i += 1
                self.progressBar(i)
            for j in range(6) :
                self.createImages(j)
        except :
            return True
        return True
   
    def createImages(self, id) :
        if id >= 0 and id < 6 :
            self.figures[id].savefig('DB/predPhotos/predImage' + str(id) +'.png')
            plt.close(self.figures[id])
            self.progressBar(int(id * 10 / 6))

#predict = Prediction()
#print(predict.getPrediction('2021-04-02 14:00:00', '192-168-0-176-8080'))
#predict.processPlot()
