from datetime import datetime
import sys
import os

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_file_name = f'nf-solver {timestamp}.txt'
log_dir_path = 'output'
log_file_path = os.path.join(log_dir_path, log_file_name)

try:
	os.makedirs(log_dir_path)

except FileExistsError:	#Do nothing if the directory is alread made.
	pass

log_file = open(log_file_path, 'a', encoding='utf-8')

def args_to_string(*args):
	s = ''
	for arg in args:
		s += str(arg)

	return s

def specialprint(*args):
	__builtins__['oldprint'](*args)
	log_file.write(args_to_string(*args))
	log_file.write('\n')

if 'oldprint' not in __builtins__:
	__builtins__['oldprint'] = __builtins__['print']

__builtins__['print'] = specialprint	#Override the print function to also
#write everything out to a file.