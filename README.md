### Prerequisite

* Python 3.x (Tested)


### Installation

* pip3 install pandas
* pip3 install moment
* pip3 install csv


### HOW TO USE THESE SCRIPTS

SCRIPT 1
* Script "generatePriceTrends.py" will generate weekly and monthly trends price from "dataset.csv" file.

SCRIPT 2
* Script "aggregatePriceTrends.py" will generate aggregation on the monthly trends price on the specified column (Country, Region, Variety, etc.) from "dataset-with-monthly-trends.csv" file previously generated.

[Example]

$> python3 aggregatePriceTrends.py Country

$> python3 aggregatePriceTrends.py Grades

$> python3 aggregatePriceTrends.py Region