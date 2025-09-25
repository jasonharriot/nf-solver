#This class represents a filter membrane. It stores size and type information,
#and calculates the permeate flow based on operating conditions.


from fluid import Fluid
import numpy as np
from util import *
from pretty import *

class Membrane:
	def __init__(self, name):
		self.area = 42 	#cm^2
		self.name = name
		pass

	def get_liquid_flux(self, concentration):
		return np.polyval(self.permeate_flux_poly, concentration)*self.area

	def get_rejection(self, concentration):
		pass

	def get_permeate_concentration(self, concentration):
		return np.polyval(self.permeate_concentration_poly, concentration)

	def get_permeate(self, concentration):
		return Fluid(f'{self.name}.perm', self.get_permeate_concentration(concentration), self.get_liquid_flux(concentration))

	def __str__(self):
		ret = f'{self.name} ({self.type}) A={PrettyArea(self.area)}'

		return ret

class MembraneVDNF_400(Membrane):	#Veolia Duracid, 400 psi
	def __init__(self, name):
		super().__init__(name)

		self.permeate_concentration_poly = [-.0012, .0483, .0581, .035]
		#Concentration in percent for any given concentration in percent.

		self.permeate_flux_poly = [.0069/(60*42), -.3029/(60*42), 4.0759/(60*42)]
		#Specific mass flux for any given concentration in percent. g/sec per
		#cm^2, or cm/s for pure water.

		self.type = 'VDNF 400 psi'

class MembraneTS80_400(Membrane):	#TS80, 400 psi
	def __init__(self, name):
		super().__init__(name)

		self.permeate_concentration_poly = [.0031, .0039, 0]
		self.permeate_flux_poly = [-.0612/(60*42), 1.16/(60*42), -6.98/(60*42), 14.8/(60*42)]
		self.type = 'TS80 400 psi'