from util import *

#Makes numbers pretty by limiting decimals and appending appropriate units. 

class Pretty(float):	#Prototype class
	def __init__(self, x, sigfigs=4):
		self.value = x
		self.sigfigs = sigfigs

		self.units = {
			1:	''
		}

	def __str__(self):
		for range_limit, unit_str in self.units.items():
			if abs(self.value) < range_limit:
				continue

			unit_val_str = pseudo_sig(self.value/range_limit, self.sigfigs) + ' ' + unit_str

			return unit_val_str

		return pseudo_sig(self.value, self.sigfigs) + ' ' + self.units[1]
		#Default case. Use the 1's unit.

	def __repr__(self):
		return self.__str__(self)

class PrettySI(Pretty):
	def __init__(self, c):
		super().__init__(c)

		self.units = {
			1e12: 'T',
			1e9: 'G',
			1e6: 'M',
			1e3: 'k',
			1:	'',
			1e-3: 'm',
			1e-6: 'μ',
			1e-9: 'n',
			1e-12: 'p'
		}

class PrettyConcentration(Pretty):
	def __init__(self, c):	#Concentration, in percent
		super().__init__(c)

		self.units = {
			1:	'% w/w',
			.1:	'ppt',
			1e-4: 'ppm',
			1e-7: 'ppb',
			
		}

class PrettyFlowRate(Pretty):
	def __init__(self, c):
		super().__init__(c)

		self.units = {
			1000: 'kg/sec',
			1: 'g/sec',
			#1/3600: 'g/day',
			1e-3: 'mg/sec',
			#(1e-3)/3600: 'mg/day',
			1e-6: 'μg/sec',
			#(1e-6)/3600: 'μg/day'

			1e-9: 'ng/sec'
		}


class PrettyArea(Pretty):
	def __init__(self, c):
		super().__init__(c)

		self.units = {
			pow(1e5, 2): 'km^2',
			pow(1e2, 2): 'm^2',
			1: 'cm^2',
			pow(1e-1, 2): 'mm^2',
			pow(1e-4, 2): 'μm^2',
			pow(1e-7, 2): 'nm^2'
		}