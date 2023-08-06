import sys
sys.path.append('../MachineLearningPackage/')

from pyLearnAlgorithms.load_data import LoadData
from pyLearnAlgorithms.split_data import SplitData

json_file = LoadData('tests/datasets', 'JSONfile.json')

jsonfile = json_file.load_json()

data = SplitData(jsonfile)

train, test, val = data.split_train_test_val(0.2, 0.3)

print('data size: ', jsonfile.size)
print('train size: ',train.size)
print('test size: ', test.size)
print('val size: ', val.size)

print(type(train))

train = json_file.convert_numpy_array(train)
test = json_file.convert_numpy_array(test)
val = json_file.convert_numpy_array(val)

print(type(train))
