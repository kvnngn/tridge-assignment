import csv
import moment
from datetime import datetime
import pandas as pd
import json

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def calculateTrendPrice(currentWeek, nextWeek):
	currentWeekPrice = float(currentWeek[1])
	nextWeekPrice = float(nextWeek[1])
	increase = nextWeekPrice - currentWeekPrice
	calculateTrendPrice.weeklyTrends[nextWeek[0]] = str(round((increase / nextWeekPrice) * 100, 2)) + '%'

def getMonthlyPrice(currentWeek):
	date = datetime.strptime(currentWeek[0], "%Y-%m-%d")
	month = str(date.strftime("%Y-%m") + ' (average price)')
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
        		calculateTrendPrice.weeklyTrends = {}
        	if (columnIndex == 0 and rowIndex == 0):
        		df_marks = pd.DataFrame(columns=row.keys())
        	if (columnIndex > 4):
        		if (len(column[1]) > 1 and previousColumn is not None):
        			if (days_between(column[0], previousColumn[0]) == 7):
        				calculateTrendPrice(column, previousColumn)
        			else:
        				calculateTrendPrice.weeklyTrends[previousColumn[0]] = ''
        		if (len(column[1]) > 1): # TODO: check if it's a price instead of columnIndex
        			previousColumn = column[:]
        			getMonthlyPrice(column)
        	else:
        		calculateTrendPrice.weeklyTrends[column[0]] = column[1]
        if (len(getMonthlyPrice.averagePricePerMonth) > 1):
        	for item in getMonthlyPrice.averagePricePerMonth:
        		print(item)
        print('Monthly average price',rowIndex + 3,'processed', getMonthlyPrice.averagePricePerMonth)
        print('Weekly trends price',rowIndex + 3,calculateTrendPrice.weeklyTrends)
        new_row = {**calculateTrendPrice.weeklyTrends, **getMonthlyPrice.averagePricePerMonth}
        print('NEW ROWWW',new_row)
        df_marks = df_marks.append(new_row, ignore_index=True)
    print(df_marks)
    df_marks.to_csv('dataset-with-trends.csv')
