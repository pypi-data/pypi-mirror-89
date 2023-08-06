import sys
sys.path.append('../MachineLearningPackage/')

from pyLearnAlgorithms.load_data import LoadData

csv_file = LoadData('tests/datasets', 'CreditRiscs.csv')

creditriscs = csv_file.load_csv()

print(creditriscs)

creditriscs = csv_file.convert_numpy_array(creditriscs)

print('\n', creditriscs)
