from essential import *
import numpy as np
import pandas as pd


class FastEda:

    def __init__(self, file: FileDetail) -> None:
        self.file = file


    def file_columns(self) -> SampleData:
        obj = self.file.obj
        sample_data = SampleData(10, obj.sample(10).values.tolist(), obj.columns, len(obj.columns), len(obj))
        return sample_data
    
    def quick_stat(self) -> QuickStat:
        stat = np.round(self.file.obj.describe().values.tolist(), 3).tolist()
        zipping = [(variable, data) for variable, data in zip(QuickStat().variables, stat)]
        return QuickStat(stat, zipping)


if __name__ == "__main__":
    fd = FileDetail(
                    'bank_data_processed.csv',
                    'csv', 
                    '500 bytes', 'static/dataset/bank_data_processed.csv', 
                     pd.read_csv('static/dataset/bank_data_processed.csv'))
    
    fasteda = FastEda(fd)

    print(fasteda.file_columns())