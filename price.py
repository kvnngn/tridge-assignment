import csv
import moment
from datetime import datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def getWeeklyTrends(currentWeekPrice, nextWeekPrice):
	increase = nextWeekPrice - currentWeekPrice
	print('nextWeekPrice', nextWeekPrice)
	print('currentWeekPrice', currentWeekPrice)
	return round((increase / nextWeekPrice) * 100, 2)

def getMonthlyPrice(currentWeek):
	date = datetime.strptime(currentWeek[0], "%Y-%m-%d")
	print('currentWeek', currentWeek)
	month = str(date.strftime("%Y-%m"))
	print('currentMonth', month)
	print("BEFORE", getMonthlyPrice.averagePricePerMonth.keys())
	if (month in getMonthlyPrice.averagePricePerMonth.keys()):
		getMonthlyPrice.averagePricePerMonth[month] = (getMonthlyPrice.averagePricePerMonth[month] + float(currentWeek[1])) / 2
		print("SUM getMonthlyPrice.averagePricePerMonth[month]", getMonthlyPrice.averagePricePerMonth[month])
	else:
		getMonthlyPrice.averagePricePerMonth[month] = float(currentWeek[1])
		print("NEW getMonthlyPrice.averagePricePerMonth[month]", getMonthlyPrice.averagePricePerMonth[month])

with open('dataset.csv') as f:
    reader = csv.DictReader(f)
    nextWeek = None
    getMonthlyPrice.averagePricePerMonth = {} 
    for i, row in enumerate(reader):
        for index, currentWeek in enumerate(row.items()):
        	if (i == 0):
        		print('-----------')
        		if (len(currentWeek[1]) > 1 and nextWeek is not None):
        			if (days_between(currentWeek[0], nextWeek[0]) == 7):
        				print(getWeeklyTrends(float(currentWeek[1]), float(nextWeek[1])), '%')
        		if (index > 4 and len(currentWeek[1]) > 1): # TODO check if it's a price instead of index
        			nextWeek = currentWeek[:]
        			getMonthlyPrice(currentWeek)


