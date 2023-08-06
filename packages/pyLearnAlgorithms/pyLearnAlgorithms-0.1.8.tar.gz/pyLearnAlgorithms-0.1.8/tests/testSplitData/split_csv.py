import sys
sys.path.append('../MachineLearningPackage/')

from pylearn.treat_data.load_data import LoadData
from pylearn.treat_data.split_data import SplitData

csv_file = LoadData('tests/datasets', 'CreditRiscs.csv')
creditriscs = csv_file.load_csv()

data = SplitData(creditriscs)

train, test, val = data.split_train_test_val(0.2, 0.3)

print('data size: ', creditriscs.size)
print('train size: ',train.size)
print('test size: ', test.size)
print('val size: ', val.size)

print(type(train))

train = csv_file.convert_numpy_array(train)
test = csv_file.convert_numpy_array(test)
val = csv_file.convert_numpy_array(val)

print(type(train))