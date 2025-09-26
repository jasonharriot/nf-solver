#This function evaluates a type-1.0 system. Contains 4 stages, 2 interstages.
#See diagram.

from filterstage import *
from controlvolume import ControlVolume
from fluid import Fluid
from membrane import *
from pretty import *

def eval_system_2_0(params):

	FS1 = FilterStageVDNF_400('FS1')
	FS2 = FilterStageVDNF_400('FS2')
	IS2 = ControlVolume('IS2')
	FS4 = FilterStageTS80_400('FS4')

	#print(params)

	FS1.concentration = params['c1_3']
	FS2.concentration = params['c2_3']

	#Stage 1
	f1_1 = Fluid('recycled_feed', params['c0'], params['Q0'])	#Input concentration, flow rate (% w/w, g/sec)
	FS1.perscribe_input(f1_1)
	(f1_3, s1) = FS1.get_result()	#Run calculations
	#print(f1_3, net_sign_str(sign))
	f1_2 = FS1.permeate

	#Stage 2
	FS2.perscribe_input(f1_3)
	(f2_3, s2) = FS2.get_result()
	#print(f2_3, net_sign_str(sign))
	f2_2 = FS2.permeate

	#Interstage 2, permeate mixing
	IS2.perscribe_inputs([f1_2, f2_2])
	(f4_1, si2) = IS2.get_result()
	#print(f4_1, net_sign_str(sign))


	#Stage 4
	FS4.concentration = f1_1.concentration	#Try to match the feed
	#concentration, so it can be recycled directly.

	FS4.perscribe_input(f4_1)
	(f4_3, s4) = FS4.get_result()
	#print(f4_3, net_sign_str(sign))
	f4_2 = FS4.permeate

	#Mass balance check
	CV = ControlVolume('check')

	f0 = Fluid('raw_feed', f1_1.concentration, f1_1.flow_rate-f4_3.flow_rate)
	#Set up feed flow now that Inerstage 1 mixing ratio is known.

	CV.perscribe_input(f0)
	CV.perscribe_outputs([f2_3, f4_2])

	(fluid_error, error_sign) = CV.get_result()

	#print(CV)

	mass_balance_valid = CV.mass_balance_is_valid()

	results = {
		'0': f0,

		'1.1': f1_1,
		'1.2': f1_2,
		'1.3': f1_3,

		'2.2': f2_2,
		'2.3': f2_3,

		'4.1': f4_1,
		'4.2': f4_2,
		'4.3': f4_3,

		's1': s1,	#Sign of implied flow from Filter Stages 1-4
		's2': s2,
		's4': s4,
		'si2': si2,	#Sign of implied flow from Interstage 2

		'A1': PrettyArea(FS1.membrane.area),
		'A2': PrettyArea(FS2.membrane.area),
		'A4': PrettyArea(FS4.membrane.area),

		'recycling_factor': Pretty(f4_3.flow_rate/f0.flow_rate),

		'net_rejection': Pretty(100*(f0.concentration-f4_2.concentration)/f0.concentration),

		'mass_balance': mass_balance_valid
	}

	return results