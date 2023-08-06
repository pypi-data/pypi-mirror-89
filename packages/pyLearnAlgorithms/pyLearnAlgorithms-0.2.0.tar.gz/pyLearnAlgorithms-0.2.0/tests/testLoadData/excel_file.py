import sys
sys.path.append('../MachineLearningPackage/')

from pyLearnAlgorithms.load_data import LoadData

excel_file = LoadData('tests/datasets', 'Adresses.xlsx')

adresses = excel_file.load_excel()

print(adresses)

adresses = excel_file.convert_numpy_array(adresses)

print('\n', adresses)