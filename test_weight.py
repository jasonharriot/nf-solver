#Show a graphical discription of each desire function.

from weight import *
from util import *
from pretty import *

x_range = list(frange(-100, 100, 5))

functions_twopoint = [desire_within]
functions_onepoint = [desire_above, desire_below]
functions_plain = [desire_more, desire_less]

args_twopoint = (-50, 50)
arg_onepoint = 25

def test(functions, arg, name):
	for func in functions:
		print(func.__name__, name, arg)

		vals = []
		for x in x_range:
			if isinstance(arg, tuple):
				val = func(x, *arg)
			else:
				val = func(x, arg)

			vals.append(val)

		val_min = min(vals)
		val_max = max(vals)

		for i in range(0, len(vals)):
			val = vals[i]
			x = x_range[i]

			norm_val = (val-val_min)/(val_max-val_min)
			bar_str = '|' + '='*int(norm_val*40)
			print(pad(x, 6), pad(Pretty(val), 32), bar_str)

		print()


test(functions_twopoint, args_twopoint, 'Two-point')

test(functions_onepoint, arg_onepoint, 'Single-point')

test(functions_plain, (), 'Plain')