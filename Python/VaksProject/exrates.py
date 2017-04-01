# this module contains functions for exchange rate manipulations
import sys
import os.path
import urllib3
import json
import datetime

appId = ''
currenciesWebUrl = 'http://openexchangerates.org/api/currencies.json'

currenciesFilePath = os.path.join('data', 'currencies.csv')

class CurrencyDoesntExistError(Exception):
	'''
	Represents an error of unknown currency
	'''
	def __init__(self, message):
		self.message = message

def getDateFromUser():
	'''
	Gets a date from user in YYYY-MM-DD format
	Prompts the user until a valid date is inserted
	Returns a date object
	'''
	validInput = 0
	while validInput == 0:
		datestr = raw_input('Enter date in YYYY-MM-DD format: ')
		try:
			inputdate = datetime.datetime.strptime(datestr,'%Y-%m-%d')
			date = datetime.date(inputdate.year, inputdate.month, inputdate.day)
			validInput = 1
		except ValueError:
			print 'Invalid date'
	return date

def getCurrencyCodeFromUser(codeDictionary):
	'''
	Gets a currency code from user
	Prompts the user until a valid currency code is inserted
	Returns the currency code
	'''
	validInput = 0
	while validInput == 0:
		currCode = raw_input('Enter a currency code: ').strip().upper()
		if currCode in codeDictionary:
			validInput = 1
		else:
			print 'Unknown currency code'
	return currCode
	
def getAmountFromUser():
	'''
	Gets a float from user representing an amount
	Prompts the user until a valid float is inserted
	Returns the inserted
	'''
	validInput = 0
	while validInput == 0:
		amountString = raw_input('Enter amount to convert: ')
		try:
			amount = float(amountString)
			validInput = 1
		except ValueError:
			print 'Invalid amount'
	return amount

def getYearFromUser():
	'''
	Gets an integer from user representing a year
	Prompts the user until a valid year is inserted
	Returns the year
	'''
	validInput = 0
	while validInput == 0:
		yearString = raw_input('Enter year: ')
		try:
			year = int(yearString)
			validInput = 1
		except ValueError:
			print 'Invalid year'
	return year

def getMonthFromUser():
	'''
	Gets an integer from user representing a month
	Prompts the user until a valid month is inserted
	Returns the month
	'''
	validInput = 0
	while validInput == 0:
		monthString = raw_input('Enter month: ')
		try:
			month = int(monthString)
			if month < 1 or month > 12:
				raise ValueError()
			validInput = 1
		except ValueError:
			print 'Invalid month'
	return month
	
def getCurrencyCodeListFromUser():
	'''
	Gets a currency list from user, separated by commas
	Prompts the user until at least one valid code is inserted
	Returns a list of codes
	'''
	currencies = get_currencies()
	validInput = 0
	while validInput == 0:
		codes = raw_input('Enter currency codes separated by commas: ')
		codes = [code.strip().upper() for code in codes.split(',')]
		codes = list(set(codes).intersection(set(currencies.keys())))
		if codes:
			validInput = 1
		else:
			print 'All codes were invalid'
	return codes

def _fetch_currencies():
	'''
	Downloads the currencies file from openexchangerates API
	Returns a dictionary that translates currency codes to currency names
	'''
	global currenciesWebUrl
	
	http = urllib3.PoolManager()
	response = http.request('GET',currenciesWebUrl)
	if response.status != 200:
		raise Exception('Fail to fetch currencies from webserver')
	responseJson = json.loads(response.data)
	currencies = dict()
	for attr, value in responseJson.iteritems():
		encodedAttr = attr.encode('utf-8')
		encodedValue = value.encode('utf-8')
		currencies[encodedAttr] = encodedValue
	return currencies

def _get_exrates_filepath(date):
	'''
	Gets the filepath for a rates file with a given date
	Inputs a date object of a specific date
	Returns a string with the filepath
	'''
	filename = 'rates-%s.csv'%(date)
	return os.path.join('data',filename)

def _get_exrates_address(date):
	'''
	Gets the api address for a rates file
	Inputs a date object of a specific date
	Returns a string with api address
	'''
	global appId
	
	return 'http://openexchangerates.org/api/historical/%s.json?app_id=%s'%(date,appId)

def _fetch_exrates(date):
	'''
	Downloads the rates file for a given date
	Inputs a date object of a specific date
	Returns a dictionary with currency codes as keys and exchange rates as values
	'''
	http = urllib3.PoolManager()
	url = _get_exrates_address(date)
	response = http.request('GET', url)
	if response.status != 200:
		raise Exception('Fail to fetch exchange rates from address %s: %s'%(url,response.data))
	responseJson = json.loads(response.data)
	rates = dict()
	for attr, value in responseJson['rates'].iteritems():
		encodedAttr = attr.encode('utf-8')
		rates[encodedAttr] = value
	return rates

def _save_currencies(currencies):
	'''
	Creates and saves data to a currencies file
	Inputs a currencies dictionary object
	'''
	global currenciesFilePath
	
	currenciesFile = open(currenciesFilePath, 'w')
	currenciesFile.write('Code, Name\n')
	for code in currencies.keys():
		currenciesFile.write('%s, %s\n'%(code,currencies[code]))
	currenciesFile.close()
	return
	
def _save_exrates(date, rates):
	'''
	Creates and saves data to a rates file
	Inputs the relevant date and the rates dictionary object
	'''
	ratesFile = open(_get_exrates_filepath(date),'w')
	ratesFile.write('Code, Rate\n')
	for code in rates.keys():
		ratesFile.write('%s, %s\n'%(code,rates[code]))
	ratesFile.close()
	return
	
def _load_currencies():
	'''
	Loads the currencies file to memory
	Returns a currencies dictionary object
	'''
	global currenciesFilePath
	
	currenciesFile = open(currenciesFilePath, 'r')
	
	currencies = dict()
	first = 1
	for line in currenciesFile:
		if first == 1:
			first = 0
			continue
		parts = line.split(', ')
		currencies[parts[0]] = parts[1].strip()
		
	return currencies

def _load_exrates(date):
	'''
	Loads a rates file to memory from a specific date
	Returns a rates dictionary object
	'''
	ratesFile = open(_get_exrates_filepath(date), 'r')
	
	rates = dict()
	first = 1
	for line in ratesFile:
		if first == 1:
			first = 0
			continue
		parts = line.split(', ')
		rates[parts[0]] = float(parts[1].strip())
		
	return rates
	
def get_currencies():
	'''
	Download/loads the currencies data
	Returns a currencies dictionary object
	'''
	global currenciesFilePath
	
	if not os.path.exists(currenciesFilePath):
		currencies = _fetch_currencies()
		_save_currencies(currencies)
	else:
		currencies = _load_currencies()
	
	return currencies

def get_exrates(date):
	'''
	Download/loads rates data from a specific date
	Inputs a date object
	Returns a rates object for the given date
	'''
	if not os.path.exists(_get_exrates_filepath(date)):
		rates = _fetch_exrates(date)
		_save_exrates(date, rates)
	else:
		rates = _load_exrates(date)
	
	return rates

def convert(amount, from_curr, to_curr, date):
	'''
	Converts between currencies
	Inputs the amount to convert, the source currency code, the target currency code and the date when the conversion is performed
	Outputs the converted amount
	'''
	rates = get_exrates(date)
	if not from_curr in rates:
		raise CurrencyDoesntExistError('Database does not contain data on ' + from_curr + ' for ' + str(date))
	if not to_curr in rates:
		raise CurrencyDoesntExistError('Database does not contain data on ' + to_curr + ' for ' + str(date))
	
	toValue = rates[to_curr]
	fromValue = rates[from_curr]
	
	return amount*toValue/fromValue

def _module_start_up():
	'''
	Runs on module startup
	Loads the application api id from app.id file and creates data folders
	'''
	try:
		global appId
		
		if not os.path.exists('app.id'):
			raise Exception('Missing app.id file')
		appIdFile = open('app.id','r')
		appId = appIdFile.read().strip()
		appIdFile.close()
		
		if not os.path.exists('data'):
			os.makedirs('data')
	except Exception as e:
		sys.stderr.write('Failed to retrieve currency codes from user: %s'%(e))
		sys.exit(-17)
		
_module_start_up()