import csv
import moment
from datetime import datetime
import pandas as pd

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def getWeeklyTrends(currentWeek, nextWeek):
	if (days_between(column[0], previousColumn[0]) == 7):
		currentWeekPrice = float(currentWeek[1])
		nextWeekPrice = float(nextWeek[1])
		increase = nextWeekPrice - currentWeekPrice
		getWeeklyTrends.weeklyTrends[nextWeek[0]] = str(round((increase / nextWeekPrice) * 100, 2)) + '%'
	else:
		getWeeklyTrends.weeklyTrends[nextWeek[0]] = ''

def getMonthlyPrice(currentWeek):
	date = datetime.strptime(currentWeek[0], "%Y-%m-%d")
	month = str(date.strftime("%Y-%m"))
	if (month in getMonthlyPrice.averagePricePerMonth.keys()):
		getMonthlyPrice.averagePricePerMonth[month] = (getMonthlyPrice.averagePricePerMonth[month] + float(currentWeek[1])) / 2
	else:
		getMonthlyPrice.averagePricePerMonth[month] = float(currentWeek[1])

with open('dataset.csv') as f:
    reader = csv.DictReader(f)
    previousColumn = None
    for rowIndex, row in enumerate(reader):
        for columnIndex, column in enumerate(row.items()):
        	if (columnIndex == 0):
        		getMonthlyPrice.averagePricePerMonth = {}
        		getWeeklyTrends.weeklyTrends = {}
        	if (columnIndex == 0 and rowIndex == 0):
        		df_marks = pd.DataFrame(columns=row.keys())
        	if (columnIndex > 4):
        		if (len(column[1]) > 1 and previousColumn is not None):
        			getWeeklyTrends(column, previousColumn)
        		if (len(column[1]) > 1): # TODO: check if it's a price instead of columnIndex
        			previousColumn = column[:]
        			getMonthlyPrice(column)
        print('Row weeklyTrends',rowIndex + 3,getWeeklyTrends.weeklyTrends)
        df_marks = df_marks.append(getWeeklyTrends.weeklyTrends, ignore_index=True)
    #print('Row monthly',rowIndex + 3,'processed', getMonthlyPrice.averagePricePerMonth)
    print(df_marks)
    df_marks.to_csv('dataset-with-trends.csv')
