#Individual weights for process variable constraints.

def desire_more(x):
	return -x

def desire_less(x):
	return x

def desire_at(x, center, a):	#Returns less loss for value closer to center.
	#Loss normalized to 10 at distance a from center

	return 10*((x-center)/a)**2

def desire_within(x, x_min, x_max):
	assert x_min < x_max

	if x > x_max:
		return 10*(x-x_max)

	if x < x_min:
		return -10*(x-x_min)

	return 0

def desire_above(x, x_min):
	if x < x_min:
		return -10*(x-x_min)

	return 0

def desire_below(x, x_max):
	if x > x_max:
		return 10*(x-x_max)

	return 0

