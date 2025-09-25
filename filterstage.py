#This class represents a filter stage. A filter stage has one input and two
#outputs. The prototype class abstracted for specific membranes and
#specific operating pressures.

from fluid import Fluid
from controlvolume import ControlVolume
from membrane import *
from util import *
from pretty import *

class FilterStage(ControlVolume):
	def __init__(self, name):
		super().__init__(name)

		self.permeate = Fluid(f'{self.name}.perm', 0, 0)	#This is the
		#permeate from the NF membrane.

		self.buffer = ControlVolume(f'{self.name}.buffer')	#This is the
		#concentrate tank that sits before each NF membrane.

		self.concentration = 0 	#The perscribed concentration of the buffer.

		self.rejection = 0 	#Rejection of the filter (%)

	def perscribe_input(self, f):
		super().perscribe_input(f)
		self.buffer.perscribe_input(f)

	def perscribe_output(self, f):
		raise Exception('Do not use perscribed outputs on a Filter Stage.')

	def get_result(self):
		temp_permeate = self.membrane.get_permeate(self.concentration)

		permeate_c = temp_permeate.concentration	#Only concentration can be
		#found at this point
		
		temp_input = self.get_input()	#The concentration and flow of the 
		#summed input streams(s)

		permeate_Q = temp_input.flow_rate*(temp_input.concentration - self.concentration)/(permeate_c-self.concentration)

		#Calculate membrane area needed to achieve given flow.
		self.membrane.area *= permeate_Q / temp_permeate.flow_rate	#Increase 
		#membrane area by factor that would provide given flow rate

		self.permeate.set(permeate_c, permeate_Q)

		self.rejection = 100*(temp_input.concentration-self.permeate.concentration)/temp_input.concentration

		self.buffer.clear_outputs()
		self.buffer.perscribe_output(self.permeate)

		self.clear_outputs()
		super().perscribe_output(self.permeate)	#Perscribe this output very
		#carefully, and only after calculation of permeate. Clear it before
		#asigning again. Hence why FilterStage itself has no
		#perscribe_output method. The permeate is given by the conditions,
		#leaving the concentrate to be fully constrained and implied. No 
		#other outputs need be perscribed.

		liquid_flux = 0	#g/sec
		solute_flux = 0	#g/sec

		for i in self.inputs:
			liquid_flux += i.flow_rate
			solute_flux += i.flow_rate*i.concentration/100

		for o in self.outputs:
			liquid_flux -= o.flow_rate
			solute_flux -= o.flow_rate*o.concentration/100

		#print(f'[ControlVolume] Result: {pretty_flow_rate(liquid_flux)}, Solute: {pretty_flow_rate(solute_flux)}')

		if not liquid_flux == 0:
			res_conc = 100*solute_flux/liquid_flux
		else:
			res_conc = 0

		res = Fluid(f'{self.name}.net', res_conc, abs(liquid_flux))

		return (res,  -net_sign(liquid_flux))	#Result fluid and sign. Sign is
		#positive for liquid entering the stage.

	def __str__(self):
		ret = f'*======== [FilterStage "{self.name}"] ========*\n'

		ret += 'Whole stage:\n'
		ret += super().__str__() + '\n'

		ret += f'Concentrate CV:\n{self.buffer}Concentrate: {pretty_concentration(self.concentration)}\n'

		ret += f'Membrane: {self.membrane}\n'

		ret += f'Permeate: {self.permeate}\n'

		ret += 'Rejection (%): {:.4f}\n'.format(self.rejection)

		ret += '*======*\n'

		return ret

class FilterStageVDNF_400(FilterStage):
	def __init__(self, name):
		super().__init__(name)

		self.membrane = MembraneVDNF_400(f'{self.name}.mem')

class FilterStageTS80_400(FilterStage):
	def __init__(self, name):
		super().__init__(name)

		self.membrane = MembraneTS80_400(f'{self.name}.mem')
