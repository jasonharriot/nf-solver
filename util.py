#This file contains some utility helper functions which perform various tricks.

import numpy as np

def frange(start, stop, jump):	#Generate a range of floating point numbers.
	while start < stop:
		yield start
		start += jump

def num_int_digits(x):	#Number of digits on the left of the decimal
	x = abs(int(x))

	n = 1

	while x >= 10:
		x = x/10
		n+=1

	return n

def pseudo_sig(x, n):	#Pseudo significant figures. Return string representing
# floating point number x truncated to n significant figures. Has no effect on
# integers or left side of decimal numbers. Assumes zeroes on rigt side are 
#significant. TODO: real sig figs?

	if type(x) in [int, np.int32, np.int64]:
		return '{:d}'.format(x)

	elif type(x) in [float, np.float64]:
		if abs(x) >= 1:
			n_left = num_int_digits(x)
			n_right = max(0, n-n_left)

			f_str = '{:.' + str(n_right) + 'f}'	#Format string with the decimal
			#precision inserted.

			s = f_str.format(x)

			return s

		else:	#if less than 1, display scientific.
			f_str = '{:.' + str(n-1) + 'e}'

			s = f_str.format(x)

			return s

	else:
		print('Unknown type:', type(x))
		return ''

def net_sign(x):	#Get the sign of a flow. Positive indicates flow into a
	#control volume, negative outwards. Zero for zero flow.
	if x == 0:
		return 0

	if x > 0:
		return 1

	return -1

def net_sign_str(x): #Display a string to help make sense of the sign of
	#a flow.

	if x == 0:
		return '(n/a)'

	if x > 0:
		return '(in)'

	return '(out)'

def pad(x, l):
	s = str(x)

	while len(s) < l:
		s += ' '

	return s