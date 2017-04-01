import math
import random

def sourceMean(srcFunc, srcParams, sampleSize):
	mean = 0
	for i in range(0,sampleSize):
		mean += srcFunc(srcParams)
	return mean/sampleSize
	
def sourceStd(srcFunc, srcParams, sampleSize):
	samples = list()
	mean = 0
	for i in range(0,sampleSize):
		sample = srcFunc(srcParams)
		mean += sample
		samples.append(sample)
	mean /= sampleSize
	
	meanSquare = 0
	for sample in samples:
		meanSquare += (sample - mean)*(sample - mean)
	
	return math.sqrt(meanSquare/sampleSize)
	
def normalGauss(params):
	return random.gauss(0,1)

sampleSize = int(raw_input('Please enter the sample size: '))
print 'Empirical source mean is ' + str(sourceMean(normalGauss,dict(), sampleSize))
print 'Empirical source standard deviation is ' + str(sourceStd(normalGauss,dict(), sampleSize))