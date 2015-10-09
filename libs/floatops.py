"""
Float numbers operations
"""

def decimalPoints(f, d):
	"""return a float rounded to d
	decimal points"""
	return round(f,d)

def decimalToString(f, d):
	"""return a string rounded to d
	decimal points"""
	form = ".%df" % int(d)
	return format(f,form)

def floatMultRound(f, v):
	"""find multiple of v nearest to f
	works only with floats""" 
	times = abs(f / v)
	dec = times - int(times)
	if f > 0: sign = 1
	else: sign = -1
	#print "dec: %.10f" % dec
	if dec >= .5:
		m = int(times) + 1
	else:
		m = int(times)
	#print "m: %.10f" % m
	return v * m * sign

if __name__ == "__main__":
	print floatMultRound(11, 3.0)