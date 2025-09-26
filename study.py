#This class manages the context for executing optimization on a set of system
#parameters

import numpy as np
from scipy.optimize import minimize
from weight import *
from util import *

class Study:
	def __init__(self, func, params, select):
		self.func = func
		self.params = params

		self.select_params = select	#Names of parameters which will be changed
		#to test different scenarios. All others won't.

		self.results = None

	def params_to_list(self, params, select):	#Extract select parameter
		#values from the given parameter bank

		select_param_keys = [x for x in list(params.keys()) if x in select]

		select_params = []

		for select_key in select_param_keys:
			select_params.append(params[select_key])

		return select_params


	def list_to_params(self, select_param_values, select):	#Create a full
		#parameter bank from select parameter values

		temp_params = self.params.copy()

		for i in range(0, len(select_param_values)):
			key = select[i]

			temp_params[key] = select_param_values[i]

		return temp_params

	def eval(self, params_list):
		test_params = self.list_to_params(params_list, self.select_params)
		#Make a full paramter bank, with the select parameters inserted. All
		#other parameters take default value.

		res = self.func(test_params)

		s = self.loss(res)

		self.results = res

		return s

	def minimize(self):
		optimize_result = minimize(self.eval, self.params_to_list(self.params, self.select_params))

		return optimize_result

	def loss(self, results):
		s = 0 	#This is an arbitrary loss value, which is high for results
		#which are bad, and low for results that are good. The optimizer finds
		#the lowest possible value, which corresponds with the best conditions.

		#Concentration sanity check
		fluid_list = ['0', '1.1', '1.2', '1.3', '2.2', '2.3', '3.2', '3.3', '4.1', '4.2', '4.3']

		for f in fluid_list:
			if not f in results:	#These fluid items may or may not be present
				#depending on the system type being studied. E.g. Filter stage 3
				#does not exist in System Type 2.0.

				continue


			s += desire_within(results[f].concentration, 0, 30)	#Get angry if
			#the concentration is impossible

			s += desire_above(results[f].flow_rate, 0)	#Get angry if the flow
			#rate is impossible

			#Notice that these desire functions are flat within the bounds
			#given. We don't have any preference for the process variable,
			#so long as it doesn't violate the boundary conditions.
			#

		sign_list = ['s1', 's2', 's3', 's4']

		for sign in sign_list:
			if not sign in results:
				continue

			s += desire_below(results[sign], 0)	#All Filter Stages should have
			#outward flow. Get angry otherwise.

			#The sign is a digital value, and doesn't have a
			#smooth/differentiable slope. This is abuse of the optimizer,
			#but seems to work anyway.


		A_list = ['A1', 'A2', 'A3', 'A4']

		for A in A_list:
			if not A in results:
				continue

			s += desire_above(results[A], 0)	#Get angry if membranes have
			#negative size.

		s += desire_less(results['recycling_factor'])	#Simply minimize this
		#value.

		s += desire_more(results['net_rejection'])	#Simply maximize this
		#value.

		return s

	def get_results(self):
		return self.results