import pandas as pd
from fbprophet import Prophet
import datetime
import os
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, colors
from fbprophet.plot import plot_forecast_component, plot_yearly, plot_weekly

class PredictionInfo :
    def __init__(self):
        self.ageBuffer = []
        self.agePercentBuffer = []
        self.genderBuffer = []
        self.genderPercentBuffer = []
        self.ageIntervalInfo = ["0-6", "6-12", "12-18", "18-26", 
                                "26-36", "36-48", "48-60", "60-100"]
        self.genderIntervalInfo = ["Women", "Men"]

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
        self.stringList = ["0-6 years old:    ", "6-12 years old:   ", "12-18 years old:  ", "18-26 years old:  ", "26-36 years old:  ",
                           "36-48 years old:  ", "48-60 years old:  ", "60-100 years old: ", "Women: ", "Men:   "]

        self.figures = []
        self.axises = []
        self.colorBuffer = []

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
        return self.predict()

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
        predInfo = PredictionInfo()

        self.models = []
        self.forecasts = []
        self.progressBar(-1)

        for i in range(10):
            predictdf = self.df.copy()
            if i < 8:
                predictdf['y'] = self.df['age'].apply(lambda x: self.getValue(x, i))
            else:
                predictdf['y'] = self.df['gender'].apply(lambda x: self.getValue(x, i - 8))
            predictdf.drop(['time', 'gender', 'age'], axis=1, inplace=True)
            predictdf['cap'] = predictdf['y'].max() * 1.1
            predictdf['floor'] = 0

            self.models.append(Prophet(interval_width=0.95, daily_seasonality=False, weekly_seasonality=True,
                                       yearly_seasonality=True, growth='logistic', holidays=self.holidays))

            with suppress_stdout_stderr():
                self.models[i].fit(predictdf)
            future = self.models[i].make_future_dataframe(periods=self.periodNum, freq='2H', include_history=False)
            future['cap'] = predictdf['y'].max()
            future['floor'] = 0
            self.forecasts.append(self.models[i].predict(future))
            self.forecasts[i].head()


            personPred = self.forecasts[i][['yhat']].values[self.periodNum - 1][0]
            if i < 8:
                ageSum += personPred
            else:
                genderSum += personPred
            dataList.append(personPred)

            self.colorBuffer.append(colors.to_hex('C' + str(i)))
            self.progressBar(i)

        for i in range(8):
            predInfo.ageBuffer.append(round(dataList[i], 2))
            predInfo.agePercentBuffer.append(round((dataList[i] / ageSum) * 100, 2))

        for i in range(8, 10):
            predInfo.genderBuffer.append(round(dataList[i], 2))
            predInfo.genderPercentBuffer.append(round((dataList[i] / genderSum) * 100, 2))

        json = {
                "ageBuffer": predInfo.ageBuffer,
                "agePercentBuffer": predInfo.agePercentBuffer,
                "genderBuffer": predInfo.genderBuffer,
                "genderPercentBuffer": predInfo.genderPercentBuffer,
                "ageIntervalInfo": predInfo.ageIntervalInfo,
                "genderIntervalInfo": predInfo.genderIntervalInfo,
                "colorBuffer": self.colorBuffer
        }
        return json

    def processPlot(self) :
        plt.close('all')
        self.figures = [plt.figure(figsize=(15, 8), dpi=160),plt.figure(figsize=(25, 8), dpi=160),
                        plt.figure(figsize=(15, 12), dpi=160),plt.figure(figsize=(15, 8), dpi=160),
                        plt.figure(figsize=(15, 8), dpi=160),plt.figure(figsize=(12, 12), dpi=160)]
        self.axises = []
        for i in range(6) :
            self.axises.append(self.figures[i].add_subplot(1,1,1))

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
            plt.close('all')
            return False
        plt.close('all')
        print(self.colorBuffer)
        return True
   
    def createImages(self, id) :
        if id >= 0 and id < 6 :
            self.figures[id].savefig('DB/predPhotos/predImage' + str(id) +'.png')
            plt.close(self.figures[id])
            self.progressBar(int(id * 10 / 6))

    def createStats(self) : 
        yeardata = []
        monthdata = []
        weekdata = []
        yearpercent = []
        monthpercent = []
        weekpercent = []

        for i in range(10):
            statdf = self.df.copy()
            if i < 8:
                statdf['y'] = self.df['age'].apply(lambda x: self.getValue(x, i))
            else:
                statdf['y'] = self.df['gender'].apply(lambda x: self.getValue(x, i - 8))
            statdf.drop(['time', 'gender', 'age'], axis=1, inplace=True)

            yeardf = statdf.resample('Y', on='ds').sum()
            monthdf = statdf.resample('M', on='ds').sum()
            weekdf = statdf.resample('W', on='ds').sum()
            print(weekdf)
            yeardata.append(int(yeardf['y'].mean()))
            monthdata.append(int(monthdf['y'].mean()))
            weekdata.append(int(weekdf['y'].mean()))

        ysum = sum(yeardata)
        msum = sum(monthdata)
        wsum = sum(weekdata)
        print(yeardata)
        print(monthdata)
        print(weekdata)
        for i in range(len(yeardata)) :
            yearpercent.append(round(yeardata[i] / ysum * 100, 2))
        for j in range(len(monthdata)) :
            monthpercent.append(round(monthdata[j] / msum * 100, 2))
        for k in range(len(weekdata)) :
            weekpercent.append(round(weekdata[k] / wsum * 100, 2))
        print(yearpercent)
        print(monthpercent)
        print(weekpercent)

