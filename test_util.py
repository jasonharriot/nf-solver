#Test some of the utility functions.

from util import *

print('Sigfigs:')
x=10000
while x > 1e-6:
	print(pseudo_sig(x, 4))
	print(pseudo_sig(-x, 4))

	x/=12.3456789