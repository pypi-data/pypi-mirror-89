import sys
sys.path.append('../MachineLearningPackage/')

from pyLearnAlgorithms.load_data import LoadData

json_file = LoadData('tests/datasets', 'JSONfile.json')

jsonfile = json_file.load_json()

print(jsonfile)

jsonfile = json_file.convert_numpy_array(jsonfile)

print('\n', jsonfile)
