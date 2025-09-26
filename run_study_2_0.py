from datetime import datetime
from pretty import *
import time
from system_2_0 import *
from study import *
from specialprint import *


if __name__ == '__main__':
	print(f'Nanofiltration System Evaluation @ {datetime.now()}')

	params = {	#List of all the unknown parameters needed to evaluate the
	#system start to finish

		'c0': 5, #% w/w
		'Q0': 1,	#g/sec
		'c1_3': 5,
		'c2_3': 10
	}

	select_params = ['c1_3']	#Short list of the parameters which will
	#be changed to optimize the result

	study = Study(eval_system_2_0, params, select_params)	#Create a Study to 
	#manage the context for optimization and fetching results

	print('Select parameters:', select_params)

	study_results = study.minimize()	#Execute the optimiztaion process and
	#fetch the results (of the optimization run)

	print('\n\n======== Optimization report ========')
	print(study_results)

	results = study.get_results()	#Fetch the resulting process variables

	print(f'\n\n======== System variables ========')

	variable_descriptions = {
		'0': 'Raw feedstock input',
		'2.3': 'Concentrated output',
		'4.2': 'Dilute waste output',

		'A1': 'Stage 1 membrane',
		'A2': 'Stage 2 membrane',
		'A4': 'Stage 4 membrane',

		'recycling_factor': 'Feedstock recycling factor',
		'net_rejection': 'Overall sodium sulfate rejection'
	}

	for var_name, var_value in results.items():	#Print the system variables and
		#Add a description to applicable entries

		if var_name in variable_descriptions.keys():
			print(f'\n{variable_descriptions[var_name]}')
			print(f'{var_name}:\t{var_value}\n')

		else:
			print(f'{var_name}:\t{var_value}')

	print()