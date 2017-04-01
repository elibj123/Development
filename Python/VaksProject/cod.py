# This program shows all the currencies on a given date
import exrates
import datetime
import sys
import traceback

print 'This program shows you all the currencies in a given date'

date = exrates.getDateFromUser()

try:
	rates = exrates.get_exrates(date)
	currencies = exrates.get_currencies()

	for key in sorted(rates):
		if not (key in currencies): # checks if key is in the currencies file
			print '<unknown> (%s)'%(key)
		else:
			print '%s (%s)'%(currencies[key],key)
except Exception as e:
	print 'Failed to execute program: %s'%(e)
	traceback.print_exc()