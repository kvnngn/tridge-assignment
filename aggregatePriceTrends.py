import csv
import moment
from datetime import datetime
import pandas as pd
import json
import sys

def getAverage(lst):
	if (len(lst) == 0):
		return ''
	return sum(lst) / len(lst)

if (len(sys.argv) > 1):
	requestedColumn = sys.argv[1]
	with open('dataset-with-monthly-trends.csv') as f:
	    reader = csv.DictReader(f)
	    trendsPerVariety = {}
	    pf = pd.DataFrame()
	    for rowIndex, row in enumerate(reader):
	        for columnIndex, column in enumerate(row.items()):
	            if (row[requestedColumn] not in trendsPerVariety.keys()):
	                trendsPerVariety[row[requestedColumn]] = {}
	            if (columnIndex > 4 and len(column[1]) > 1):
	                if (column[0] not in trendsPerVariety[row[requestedColumn]].keys()):
	                    trendsPerVariety[row[requestedColumn]][column[0]] = []
	                trendsPerVariety[row[requestedColumn]][column[0]].append(float(column[1]))
	    for variety, values in trendsPerVariety.items():
	    	for date in values:
	    		values[date] = round(getAverage(values[date]), 2)
	    	values[requestedColumn] = variety
	    	pf = pf.append(values, ignore_index=True)
	pf = pf.reindex(sorted(pf.columns, reverse=True), axis=1)
	print('Generating CSV file with weekly trends...')
	pf.to_csv('agregation-with-trends-on-' + requestedColumn + '.csv', index=False)
	print("File 'agregation-with-trends-on-" + requestedColumn +".csv' generated.")
else:
	print('[USAGE] python3 aggregatePriceTrends.py [requestedColumn]\n')
	print('[Example]\npython3 aggregatePriceTrends.py Country\npython3 aggregatePriceTrends.py Grades\npython3 aggregatePriceTrends.py Region')

        

