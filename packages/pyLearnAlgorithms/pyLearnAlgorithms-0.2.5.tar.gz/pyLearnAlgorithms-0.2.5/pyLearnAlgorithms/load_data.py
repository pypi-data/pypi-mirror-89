import pandas as pd 
from scipy.io import loadmat
import numpy as np
import os

class LoadData():
    """class responsible for loading various data formats"""

    def __init__(self, path, path_file):
        """set the name and location of the file"""

        # directory where the file is located
        self.path = path
        # data file name
        self.path_file = path_file

        return None

    def load_csv(self):
        """function that opens csv files"""

        csv_path = os.path.join(self.path, self.path_file)

        return pd.read_csv(csv_path)
    
    def load_excel(self):
        """function that opens excel files"""

        excel_path = os.path.join(self.path, self.path_file)

        return pd.read_excel(excel_path)

    def load_json(self):
        """function that opens json files"""

        json_path = os.path.join(self.path, self.path_file)

        return pd.read_json(json_path)
    
    def load_mat(self):
        """function that opens matlab files"""

        mat_path = os.path.join(self.path, self.path_file)

        return loadmat(mat_path)
    
    def load_txt(self):
        """function that opens text files"""

        txt_path = os.path.join(self.path, self.path_file)

        return pd.read_csv(txt_path, header = None)

    def convert_numpy_array(self, data):
        """turns a data file into a numpy array"""
        
        data = np.array(data)

        return data