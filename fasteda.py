import pandas as pd
from essential import *
import numpy as np


def file_columns(filedetail: FileDetail) -> SampleData:
    obj = filedetail.obj
    sample_data = SampleData(10, obj.sample(10).values.tolist(), obj.columns, len(obj.columns), len(obj))
    return sample_data


def quick_stat(filedetail: FileDetail) -> QuickStat:
    stat = np.round(filedetail.obj.describe().values.tolist(), 3).tolist()
    zipping = [(variable, data) for variable, data in zip(QuickStat().variables, stat)]
    return QuickStat(stat, zipping)


if __name__ == "__main__":
    fd = FileDetail(
                    'bank_data_processed.csv',
                    'csv', 
                    '500 bytes', 'static/dataset/bank_data_processed.csv', 
                     pd.read_csv('static/dataset/bank_data_processed.csv'))
    
    print(quick_stat(fd).zipped)