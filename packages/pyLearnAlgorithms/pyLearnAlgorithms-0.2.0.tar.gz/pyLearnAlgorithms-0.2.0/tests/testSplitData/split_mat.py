import sys
sys.path.append('../pyLearnAlgorithms/')

from pyLearnAlgorithms.load_data import LoadData
from pyLearnAlgorithms.split_data import SplitData

matlab_file = LoadData('tests/datasets', 'WaterLevel.mat')

waterlevel = matlab_file.load_mat()

data = SplitData(waterlevel)

train, test = data.split_train_test(0.2)
