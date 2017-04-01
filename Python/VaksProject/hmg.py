# This program allows you to generate a change graph for certain currencies
import exrates
import datetime
import sys
import traceback
import calendar

print 'This program allows you to generate a change graph for certain currencies'


# input year and month and calculate number of days using calendar module
year = exrates.getYearFromUser()
month = exrates.getMonthFromUser()
numDays = calendar.monthrange(year,month)[1]

try:
	currencyCodes = exrates.getCurrencyCodeListFromUser()
except Exception as e:
	print 'Failed to retrieve currency codes from user: %s'%(e)
	traceback.print_exc()
	sys.exit(-17)

print 'Processing the codes...'
try:
	# this is the title line in the csv file
	csvText= 'Date'
	for code in currencyCodes:
		csvText += ',' + code
	csvText += '\n'
	
	# the initial change value for each currency is 0
	csvText += str(datetime.date(year,month,1))
	for code in currencyCodes:
		csvText += ',0'
	csvText += '\n'
	
	previousRates = exrates.get_exrates(datetime.date(year,month,1))
	for day in range(2,numDays+1):
		currDate = datetime.date(year,month,day)
		rates = exrates.get_exrates(currDate)
		csvText += str(currDate)
		for code in currencyCodes:
			# compare the current rate to the previous rate
			if code in rates:
				if code in previousRates:
					change = 100*(rates[code]/previousRates[code] - 1) # computes the change in percentage
					csvText += ',' + str(change)
				else: # initialize the currency change to 0
					csvText += ',0'
			else: # no information on the currency in the current date
				csvText += ',-'
		csvText += '\n'
		previousRates = rates
		
	filename = raw_input('Enter a filename without extension: ')
	saveFile = open(filename + '.csv','w')
	saveFile.write(csvText)
	saveFile.close()
except Exception as e:
	print 'Unable to execute hist program: %s'%(e)
	traceback.print_exc()
	