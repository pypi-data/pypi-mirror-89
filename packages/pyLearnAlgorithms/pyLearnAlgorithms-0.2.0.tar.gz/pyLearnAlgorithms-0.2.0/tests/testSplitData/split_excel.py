import sys
sys.path.append('../MachineLearningPackage/')

from pyLearnAlgorithms.load_data import LoadData
from pyLearnAlgorithms.split_data import SplitData

excel_file = LoadData('tests/datasets', 'Adresses.xlsx')

adresses = excel_file.load_excel()

data = SplitData(adresses)

train, test, val = data.split_train_test_val(0.2, 0.3)

print('data size: ', adresses.size)
print('train size: ',train.size)
print('test size: ', test.size)
print('val size: ', val.size)

print(type(train))

train = excel_file.convert_numpy_array(train)
test = excel_file.convert_numpy_array(test)
val = excel_file.convert_numpy_array(val)

print(type(train))

