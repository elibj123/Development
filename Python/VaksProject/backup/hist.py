import exrates
import datetime
import sys
import traceback

print 'This program allows you to save the history'

# input the dates and sort them
print 'Please enter first date:\n' 
date1 = exrates.getDateFromUser()

print 'Please enter second date:\n'
date2 = exrates.getDateFromUser()
if date1 < date2:
	start_date = date1
	end_date = date2
else:
	start_date = date2
	end_date = date1

try:
	currencyCodes = exrates.getCurrencyCodeListFromUser()
except Exception as e:
	print 'Failed to retrieve currency codes from user: %s'%(e)
	traceback.print_exc()
	sys.exit(-17)

print 'Processing the codes...'


try:
	# this is the titles in the csv file
	csvText= 'Date'
	for code in currencyCodes:
		csvText += ',' + code
	csvText += '\n'
	
	days = [start_date + datetime.timedelta(days=x) for x in range((end_date-start_date).days + 1)]	 # generate the date range
	# generate each line in the csv file
	for day in days:
		rates = exrates.get_exrates(day)
		csvText += str(day)
		for code in currencyCodes:
			if code in rates: # checks if data exists for this currency code in the specific date
				csvText += ',' + str(rates[code])
			else:
				csvText += ',-'
		csvText += '\n'
		
	filename = raw_input('Enter a filename without extension: ')
	
	saveFile = open(filename + '.csv','w')
	saveFile.write(csvText)
	saveFile.close()
except Exception as e:
	print 'Unable to execute hist program: %s'%(e)
	traceback.print_exc()
	