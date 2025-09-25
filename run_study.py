from datetime import datetime
from pretty import *
import time
from system_1_0 import *
from study import *


if __name__ == '__main__':
	print('\n'*10)
	print(f'Nanofiltration System Evaluation @ {datetime.now()}')

	params = {
		'c0': .4, #% w/w
		'Q0': 1,	#g/sec
		'c1_3': 3,
		'c2_3': 7,
		'c3_3': 10
	}

	select_params = ['c1_3', 'c2_3']

	study = Study(eval_system_1_0, params, select_params)

	print('Select parameters:', select_params)

	print('Optimizing...')

	study_results = study.minimize()	#Execute the optimiztaion process and
	#fetch results

	results = study.get_results()	#Fetch the process variables

	print('Optimized parameters:', study_results['x'])

	print('='*32)
	print(f'System variables')

	for var_name, fluid in results.items():
		print(f'{var_name}:\t{fluid}')

	print()

	print('System summary')

	print('Stock recycling factor:', '{:.2f}'.format(results['recycling_factor']))
	print('Overall waste sodium rejection (%): {:.2f}'.format(results['net_rejection']))
	print('Raw feed:', results['0'])
	print('Concentrate:', results['3.3'])
	print('Waste permeate:', results['4.2'])