# preprocess/data_load.py

import pandas as pd
import os

class DataLoader:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir

    def load_air_quality(self):
        path = os.path.join(self.data_dir, '대기오염(구별)_20250512104916.csv')
        return pd.read_csv(path)

    def load_green_area(self):
        path = os.path.join(self.data_dir, '녹지현황_20250512110012.csv')
        return pd.read_csv(path)

    def load_waste_data(self):
        path = os.path.join(self.data_dir, '쓰레기수거+현황_20250512111736.csv')
        return pd.read_csv(path)
