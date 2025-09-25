#This class represents a control volume of fluid. It may have any number of 
#inputs and outputs. The mass balance can be checked and the implied in/outputs
#calculated.


from fluid import Fluid
from util import *
from pretty import *

class ControlVolume:
	def __init__(self, name):
		self.name = name
		self.inputs = []
		self.outputs = []

	def perscribe_input(self, fluid):
		#print(f'Control volume input: {fluid}')
		self.inputs.append(fluid)

	def perscribe_output(self, fluid):
		self.outputs.append(fluid)

	def perscribe_inputs(self, fluids):
		for fluid in fluids:
			self.perscribe_input(fluid)

	def perscribe_outputs(self, fluids):
		for fluid in fluids:
			self.perscribe_output(fluid)

	def get_input(self):
		liquid_flux = 0	#g/sec
		solute_flux = 0	#g/sec

		for i in self.inputs:
			liquid_flux += i.flow_rate
			solute_flux += i.flow_rate*i.concentration/100

		if not liquid_flux == 0:
			res_conc = 100*solute_flux/liquid_flux
		else:
			res_conc = 0

		res = Fluid(f'{self.name}.net_in', res_conc, liquid_flux)

		return res

	def get_output(self):
		liquid_flux = 0	#g/sec
		solute_flux = 0	#g/sec

		for o in self.outputs:
			liquid_flux += o.flow_rate
			solute_flux += o.flow_rate*o.concentration/100

		if not liquid_flux == 0:
			res_conc = 100*solute_flux/liquid_flux
		else:
			res_conc = 0

		res = Fluid(f'{self.name}.net_out', res_conc, liquid_flux)

		return res

	def clear_inputs(self):
		self.inputs = []

	def clear_outputs(self):
		self.outputs = []

	def get_result(self):
		liquid_flux = 0	#g/sec
		solute_flux = 0	#g/sec

		for i in self.inputs:
			liquid_flux += i.flow_rate
			solute_flux += i.flow_rate*i.concentration/100

		for o in self.outputs:
			liquid_flux -= o.flow_rate
			solute_flux -= o.flow_rate*o.concentration/100
		
		if not liquid_flux == 0:
			res_conc = 100*solute_flux/liquid_flux
		else:
			res_conc = 0

		res = Fluid(f'{self.name}.net', res_conc, abs(liquid_flux))

		return (res, -net_sign(liquid_flux))	#Result fluid and sign.

	def mass_balance_is_valid(self):
		threshold = 1e-8

		f, s = self.get_result()

		return f.flow_rate < threshold

	def __str__(self):
		(res_fluid, sign) = self.get_result()

		ret = f'======== [ControlVolume "{self.name}"] ========\nInputs:\n'

		ii = 0
		for i in self.inputs:
			ret += f'{ii}\t{i}\n'
			ii+=1

		ret += 'Outputs:\n'

		ii=0
		for o in self.outputs:
			ret += f'{ii}\t{o}\n'
			ii+=1

		ret += 'Implied result:\n'

		
		sign_str = net_sign_str(sign)

		ret += f'0\t{res_fluid} {sign_str}\n'

		#good = self.mass_balance_is_valid()

		#ret += f'Mass balance: {'GOOD' if good else 'BAD'}\n'

		ret += '========\n'

		return ret
