from essential import *
import numpy as np
import pandas as pd

class FastEda:

    def __init__(self, file: FileDetail) -> None:
        self.file = file
        self.obj = file.obj

    def file_columns(self) -> SampleData:
        obj = self.obj
        sample_data = SampleData(10, obj.sample(10).values.tolist(), obj.columns, len(obj.columns), len(obj))
        return sample_data
    
    def quick_stat(self) -> QuickStat:
        stat = np.round(self.file.obj.describe().values.tolist(), 3).tolist()
        numerical_col = self.file.obj.select_dtypes(exclude = ['object']).columns.to_list()
        zipping = [(variable, data) for variable, data in zip(QuickStat().variables, stat)]
        return QuickStat(stat, numerical_col, zipping)

    def correlation(self) -> Correlation:
        v = self.obj.corr().index.to_list()
        corr = np.round(self.obj.corr().values, 2).tolist()
        return Correlation(variable = v,
                            correlation = corr)


if __name__ == "__main__":
    fd = FileDetail(
                    'bank_data_processed.csv',
                    'csv', 
                    '500 bytes', 'static/dataset/cars.csv', 
                     pd.read_csv('static/dataset/cars.csv'))
    
    fasteda = FastEda(fd)
    print(fasteda.quick_stat().numerical_col)
    # process = IndividualVariable(fd)
    # process.start()
    # print(process.full_variables.length)