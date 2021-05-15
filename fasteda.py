from essential import *
import numpy as np
import pandas as pd
from eda_report.univariate import Variable
import tqdm


class IndividualVariable():

    def __init__(self, filedetail: FileDetail):
        self.filedetail = filedetail
        self.data = filedetail.obj
        self.full_variables = IndividualVariables(length=0)
    
    def start(self):
        for i in tqdm.tqdm(self.filedetail.obj.columns, desc="Univariate Analysing"):
            v = Variable(self.data[i])
            variable = VariableDetail(
                            vname=i,
                            missing=v.missing,
                            vtype=v.var_type,
                            vsummary=(v.statistics.index.to_list(), v.statistics.values.tolist()))
            self.full_variables.Variables.append(variable)
            self.full_variables.length += 1
            
        assert self.full_variables.length == len(self.data.columns), "Length counter value and total number of columns is different"

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
    process = IndividualVariable(fd)
    process.start()
    print(process.full_variables.length)