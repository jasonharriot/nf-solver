#Evaluate the system at a single configuration.

from datetime import datetime
from pretty import *
import time
from system_1_0 import *

print('\n'*10)
print(f'Nanofiltration System Evaluation @ {datetime.now()}')


if __name__ == '__main__':
	params = {
		'c0': 1, #% w/w
		'Q0': 1,	#g/sec
		'c1_3': 3,
		'c2_3': 7,
		'c3_3': 10
	}

	results = eval_system_1_0(params)

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