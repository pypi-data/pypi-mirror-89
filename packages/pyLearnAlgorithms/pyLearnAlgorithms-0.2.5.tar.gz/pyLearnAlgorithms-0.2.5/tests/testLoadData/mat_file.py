import sys
sys.path.append('../pyLearnAlgorithms/')

from pyLearnAlgorithms.load_data import LoadData

matlab_file = LoadData('tests/datasets', 'WaterLevel.mat')

waterlevel = matlab_file.load_mat()

print(waterlevel)

waterlevel = matlab_file.convert_numpy_array(waterlevel)

print('\n', waterlevel)
