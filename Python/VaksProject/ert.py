# This program shows you all the currency values in a given date

import exrates
import datetime
import sys

print 'This program shows you all the currency values in a given date'
date = exrates.getDateFromUser()

try:
	rates = exrates.get_exrates(date)
	currencies = exrates.get_currencies()
	
	titles = ['Currency Name', 'Currency Value']
	
	lineSize = 100
	
	# print the table so that the right column is aligned to the left (length of line is 100)
	print '%s%s'%(titles[0],titles[1].rjust(lineSize - len(titles[0])))
	print '-'*lineSize
	for key in sorted(rates):
		if not (key in currencies): # check if key is in currencies fiel
			name = '<unknown> (%s)'%(key)
		else:
			name = '%s (%s)'%(currencies[key],key)
		rate = '%.5f'%(rates[key])
		
		# print line with right column adjusted to maintain a constant line length
		print '%s%s'%(name,rate.rjust(lineSize-len(name)))
	print '-'*lineSize
except Exception as e:
	print 'Failed to execute program ert: %s'%(e)
	traceback.print_exc()
