# This program inputs two currencies and converts an amount between them
import exrates
import datetime
import sys
import traceback

print 'This program allows you to convert between currencies'
date = exrates.getDateFromUser()

try:
	rates = exrates.get_exrates(date)
except Exception as e:
	print 'Failed to load exchange rates: %s'%(e)
	traceback.print_exc()
	sys.exit(-17)

currCode1 = exrates.getCurrencyCodeFromUser(rates)
currCode2 = exrates.getCurrencyCodeFromUser(rates)
amount = exrates.getAmountFromUser()

try:
	# convert in both directions
	in_curr1 = exrates.convert(amount,currCode2,currCode1,date)
	in_curr2 = exrates.convert(amount,currCode1,currCode2,date)
	
	# show the results
	print '%f %s is %f %s'%(amount, currCode2, in_curr1, currCode1)
	print '%f %s is %f %s'%(amount, currCode1, in_curr2, currCode2)
except Exception as e:
	print 'Failed to load exchange rates: %s'%(e)
	traceback.print_exc()