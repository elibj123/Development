# This program shows the maximal and minimal rates for a list of currencies
import exrates
import datetime
import sys
import traceback
import calendar

# prints four strings in an adjusted table
def print_rjusted(s1, s2, s3, s4):
	print '%s%s%s%s'%(s1, s2.rjust(40-len(s1)), s3.rjust(40 - len(s2)), s4.rjust(40 - len(s3)))
	return

print 'This program allows you to analysis the change in exchange rate of certain currencies'

# Input dates and sort them
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
	days = [start_date + datetime.timedelta(days=x) for x in range((end_date-start_date).days + 1)] # generates the date range
	dailyRates = [exrates.get_exrates(day) for day in days] # generates a list of rates objects for the date range
	codeStatistics = list()
	
	for currIndex in range(0,len(currencyCodes)):
		# analyze each currency in the list
		maxRate = 0
		minRate = float('inf')
		code = currencyCodes[currIndex]
		found = 0
		for rates in dailyRates:
			if code in rates:
				found = 1
				if rates[code] > maxRate:
					maxRate = rates[code]
				if rates[code] < minRate:
					minRate = rates[code]
		
		if found:
			codeStatistics.insert(0, {'max':maxRate,'min':minRate,'diff':maxRate-minRate,'code':code})
	
	if not codeStatistics:
		raise Exception('None of the codes had data on these dates')
		
	# print the table
	print_rjusted('Currency Code','Max. Rate','Min. Rate','Diff')
	for statistic in sorted(codeStatistics, key = lambda x: x['diff'], reverse = True): # this sorts the list by the diff value
		maxstr = '%.5f'%(statistic['max'])
		minstr = '%.5f'%(statistic['min'])
		diffstr = '%.5f'%(statistic['diff'])
		codestr = statistic['code']
		print_rjusted(codestr,maxstr,minstr,diffstr)
		
except Exception as e:
	print 'Unable to execute hist program: %s'%(e)
	traceback.print_exc()
	