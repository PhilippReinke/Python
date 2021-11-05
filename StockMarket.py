import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import datetime
from operator import itemgetter
from beautifultable import BeautifulTable

### some functions	
def niceDateTime(s):
	return s[:10] + " " + s[11:16]
def day_of_week_num(dts):
	# 0 = monday
    return (dts.astype("datetime64[D]").view("int64") - 4) % 7
num2day = {0:"Montag", 1:"Dienstag", 2:"Mittwoch", 3:"Donnerstag", 4:"Freitag", 5:"Samstag", 6:"Sonntag"}

### get data
stocks   = "AMZN TSLA"
df 	     = yf.download(stocks, period="5d", interval="1m", progress=False)

from forex_python.converter import CurrencyRates
c = CurrencyRates()
dollar_euro = c.get_rate("USD", "EUR")
print( "\nDollar to Euro (current): " + str(dollar_euro) + "\n" )

### format and seperate date and time
dateTime = df.index.values
day = dateTime[0]
dateDay = [day_of_week_num(ele) for ele in dateTime]

### plot graphs
for stock in stocks.split():
	plt.title(stock)
	adjClose = df["Adj Close"][stock].tolist()
	plt.plot( adjClose )
	#plt.show()

### check some properties
for stock in stocks.split():

	print(" === " + str(stock) + " ===")

	# min and max
	adjClose = np.array(df["Adj Close"][stock])*dollar_euro
	idxMin = min(enumerate(adjClose), key=itemgetter(1))[0]
	idxMax = max(enumerate(adjClose), key=itemgetter(1))[0]

	# fill table
	table = BeautifulTable()
	table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)

	table.rows.append(["gesamter Zeitraum", "EUR", ""])
	table.rows.append(["Minimum", adjClose[idxMin], niceDateTime(str(dateTime[idxMin]))])
	table.rows.append(["Maximum", adjClose[idxMax], niceDateTime(str(dateTime[idxMax]))])

	# print table
	print(table)
	print("")