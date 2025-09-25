#This class represents the fluid at a point in the system, without regard for
#direction, volume, etc. Concentration is given in percent mass, and flow rate
#in grams per second.

from util import *
from pretty import *

class Fluid:
	def __init__(self, name='noname', concentration=0, flow_rate=0):
		self.name = name
		self.set(concentration, flow_rate)

	def set(self, concentration, flow_rate):
		self.set_concentration(concentration)
		self.set_flow_rate(flow_rate)

	def set_concentration(self, concentration):
		#if concentration < 0:
		#	raise Exception(f'Impossible fluid parameter: {pretty_concentration(concentration)}')

		self.concentration = concentration

	def set_flow_rate(self, flow_rate):
		#if flow_rate < 0:
		#	raise Exception(f'Impossible fluid parameter: {pretty_flow_rate(flow_rate)}')

		self.flow_rate = flow_rate



	def clone(self, fluid):
		self.name = fluid.name
		self.set(fluid.concentration, fluid.flow_rate)


	def __str__(self):
		return f'"{self.name}"\t{PrettyConcentration(self.concentration)},\t{PrettyFlowRate(self.flow_rate)}'