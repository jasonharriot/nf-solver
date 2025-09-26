#Test some aspects of the Fluid class

from util import *
from membrane import *
from controlvolume import *

test_membrane = MembraneVDNF_400('Test Membrane 1')
p = test_membrane.get_permeate(10)
print('Test membrane:', p)

test_cv = ControlVolume('Test CV 1')
f1_1 = Fluid('1.1', 1, 10)
f1_2 = Fluid('1.2', 5.02, 1)

test_cv.perscribe_input(f1_1)
test_cv.perscribe_output(f1_2)

f1_3 = test_cv.get_result()

print(test_cv)

try:
	Fluid('Impossible 1', -1, 1)
except Exception as e:
	print(e)

try:
	Fluid('Impossible 2', 1, -1)
except Exception as e:
	print(e)

