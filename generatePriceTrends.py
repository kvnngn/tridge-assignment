import csv
import moment
from datetime import datetime
import pandas as pd
import json

def days_between(d1, d2):
	d1 = datetime.strptime(d1, "%Y-%m-%d")
	d2 = datetime.strptime(d2, "%Y-%m-%d")
	return abs((d2 - d1).days)

def diff_month(d1, d2):
	d1 = datetime.strptime(d1, '%Y-%m')
	d2 = datetime.strptime(d2, '%Y-%m')
	return (d1.year - d2.year) * 12 + d1.month - d2.month

def calculateTrendPrice(currentWeek, nextWeek):
	try:
		currentWeekPrice = float(currentWeek[1])
		nextWeekPrice = float(nextWeek[1])
		increase = nextWeekPrice - currentWeekPrice
		return str(round((increase / nextWeekPrice) * 100, 2))
	except ValueError:
		pass

def getMonthlyPrice(currentWeek):
	date = datetime.strptime(currentWeek[0], "%Y-%m-%d")
	month = str(date.strftime("%Y-%m"))
	if (len(currentWeek[1]) > 0):
		if (month not in getMonthlyPrice.averagePricePerMonth.keys()):
			getMonthlyPrice.averagePricePerMonth[month] = []
		getMonthlyPrice.averagePricePerMonth[month].append(float(currentWeek[1]))
	else:
		getMonthlyPrice.averagePricePerMonth[month] = []

def getAverage(lst):
	if (len(lst) == 0):
		return ''
	return sum(lst) / len(lst)

with open('dataset.csv') as f:
    reader = csv.DictReader(f)
    previousColumn = None
    for rowIndex, row in enumerate(reader):
        for columnIndex, column in enumerate(row.items()):
        	if (columnIndex == 0): # TODO: reset value before second loop instead of using if condition
        		print('[PROCESSING] Calculating wekekly price trends for row',rowIndex, '...')
        		getMonthlyPrice.averagePricePerMonth = {}
        		calculateTrendPrice.weeklyTrends = {}
        		monthlyTrends = {}
        	if (columnIndex == 0 and rowIndex == 0): # TODO: reset value before second loop instead of using if condition
        		df_weekly_trends = pd.DataFrame(columns=row.keys())
        		df_monthly_trends = pd.DataFrame(columns=list(row)[:4])
        	if (columnIndex > 4): # TODO: check if it's a price instead of using column index
        		if (len(column[1]) > 1 and previousColumn != None):
        			if (days_between(column[0], previousColumn[0]) == 7):
        				calculateTrendPrice.weeklyTrends[previousColumn[0]] = calculateTrendPrice(column, previousColumn)
        			else:
        				calculateTrendPrice.weeklyTrends[previousColumn[0]] = ''
        		previousColumn = column[:]
        		getMonthlyPrice(column)
        	else:
        		calculateTrendPrice.weeklyTrends[column[0]] = column[1]
        		monthlyTrends[column[0]] = column[1]
        if (len(getMonthlyPrice.averagePricePerMonth) > 1):
        	print('[ENDED] Weekly Price trends for row',rowIndex, 'has been calculated.')
        	print('[PROCESSING] Calculating monthly price trends for row',rowIndex, '...')
        	previousItem = None
        	for j, item in enumerate(getMonthlyPrice.averagePricePerMonth.items()):
        		if (previousItem != None and type(item[1]) != str and type(previousItem[1]) != str):
        			if (type(previousItem[1]) == list):
        				previousItem = (previousItem[0], getAverage(previousItem[1]))
        			item = (item[0], getAverage(item[1]))
        			if (diff_month(item[0], previousItem[0]) == -1):
        				month_trend = calculateTrendPrice(item, previousItem)
        				if (month_trend != None):        					
        					monthlyTrends[previousItem[0]] = month_trend
        				else:
        					monthlyTrends[previousItem[0]] = ''
        			else:
        				monthlyTrends[previousItem[0]] = ''
        		previousItem = item[:]
        	print('[ENDED] Monthly Price trends for row',rowIndex, 'has been calculated.')
        else:
        	print('Can find price to calculate weekly and monthly trends')
        df_weekly_trends = df_weekly_trends.append(calculateTrendPrice.weeklyTrends, ignore_index=True)
        df_monthly_trends = df_monthly_trends.append(monthlyTrends, ignore_index=True)
    df_weekly_trends = df_weekly_trends.reindex(sorted(df_weekly_trends.columns, reverse=True), axis=1)
    df_monthly_trends = df_monthly_trends.reindex(sorted(df_monthly_trends.columns, reverse=True), axis=1)
    print('Generating CSV file with weekly trends...')
    df_weekly_trends.to_csv('dataset-with-weekly-trends.csv', index=False)
    print("File 'dataset-with-weekly-trends.csv' generated.")

    print('Generating CSV file with monthly trends...')
    df_monthly_trends.to_csv('dataset-with-monthly-trends.csv', index=False)
    print("File 'dataset-with-monthly-trends.csv' generated.")

