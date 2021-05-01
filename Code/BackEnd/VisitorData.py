import numpy as np
import pandas as pd
import random
from datetime import datetime
from datetime import timedelta

intervals = [[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12], [12, 14], [14, 16], [16, 18], [18, 20], [20, 22], [22, 24]]

weekday_interval = [1, 2, 3, 6, 15, 32, 54, 75, 98, 123, 141, 146]
weekend_interval = [2, 3, 4, 7, 18, 41, 74, 113, 153, 188, 214, 221]

def weekIntervalRandID(isWeekDay) :
    interval = []
    if isWeekDay :
        interval = weekday_interval
    else :
        interval = weekend_interval

    num = random.randrange(interval[-1])
    for i in range(len(interval)) :
        if num < interval[i] :
            return i
    return -1


weekPercentage = [84, 179, 268, 360, 455, 564, 664]

def weekDayRandID() :
    num = random.randrange(weekPercentage[-1])
    interval = weekPercentage
    for i in range(len(interval)) :
        if num < interval[i] :
            return i
    return -1

agePercentage = [2, 6, 12, 25, 49, 67, 85, 100]

def ageRandID() :
    num = random.randrange(agePercentage[-1])
    interval = agePercentage
    for i in range(len(interval)) :
        if num < interval[i] :
            return i
    return -1

genderPercentage = [42, 100]

def genderRandID() :
    num = random.randrange(genderPercentage[-1])
    interval = genderPercentage
    for i in range(len(interval)) :
        if num < interval[i] :
            return i
    return -1

def createData(path, visitorPerWeek, numberOfWeeks, startDate) :
    firstTime = True
    dateNow = startDate
    for w in range(numberOfWeeks) :
        weekBucket = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        noise = random.randrange(int(visitorPerWeek * 0.1)) - int(visitorPerWeek * 0.05)
        for vis in range(visitorPerWeek + noise) :
            dayID = weekDayRandID()
            intervalID = weekIntervalRandID(dayID < 5)
            weekBucket[dayID][intervalID] += 1

        for day in range(7) :
            interval = weekBucket[day]

            for i in range(len(interval)) :
                ageBucket = [0, 0, 0, 0, 0, 0, 0, 0]
                genderBucket = [0, 0]

                count = interval[i]
                for j in range(count) :
                    genderID = genderRandID()
                    ageID = ageRandID()
                    ageBucket[ageID] += 1
                    genderBucket[genderID] += 1
                
                df = pd.DataFrame([[dateNow.strftime("%Y-%m-%d %H:%M:%S"), str(ageBucket), str(genderBucket)]],columns=['time', 'age', 'gender'])
                df.to_csv(path, mode='a', index=False, header=firstTime)
                firstTime = False
                dateNow = dateNow + timedelta(hours=2)

createData("DB/cameras/192-168-0-0-8080.csv", 10000, 100, datetime(2019, 2, 2, 0, 0, 0))