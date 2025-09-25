#Test the pretty functions.

from util import *
from pretty import *

k= 9.123
a=10

def row(x):
	print(pad(func(x), 24), '\t', x)


for func in [Pretty, PrettyConcentration, PrettyFlowRate, PrettyArea, PrettySI]:
	x=10**a

	print(f'======== {func.__name__} ========')

	while x > 10**-a:
		row(x)

		x /= k

	row(0)

	x = -x

	while x > -10**a:
		row(x)

		x *= k

	print()