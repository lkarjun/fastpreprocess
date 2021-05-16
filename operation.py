from eda_report.univariate import Variable
from essential import *
import tqdm
import pandas as pd
import numpy as np

class IndividualVariable():

    def __init__(self, filedetail: FileDetail):
        self.filedetail = filedetail
        self.data = filedetail.obj
        self.full_variables = IndividualVariables()
    
    def outlier(self, v, i):
        df = self.data
        q1q2 = v.statistics.iloc[[4,6]].values.flatten()
        IQR = q1q2[1] - q1q2[0]
        print('Iqr: ', i, IQR)
        outlier = df[i][(df[i] < (q1q2[0] - 1.5 * IQR)) |(df[i] > (q1q2[1] + 1.5 * IQR))].values
        return (outlier.astype(int)).tolist()
        
    def start(self):
        for i in tqdm.tqdm(self.filedetail.obj.columns, desc="Univariate Analysing"):
            v = Variable(self.data[i])
            outlier = None
            if v.var_type == 'numeric':
                outlier = self.outlier(v, i)
            
            variable = VariableDetail(
                            vname=i,
                            missing=v.missing,
                            vtype=v.var_type,
                            vsummary=(v.statistics.index.to_list(), v.statistics.values.tolist()),
                            stat=v.statistics,
                            outlier_track=outlier)
            self.full_variables.Variables.append(variable)
            self.full_variables.length += 1
        assert self.full_variables.length == len(self.data.columns), "Length counter value and total number of columns is different"



if __name__ == "__main__":
    df = pd.read_csv('static/dataset/cars.csv', delimiter=',')
    sub_df = df[[' time-to-60', ' brand']].copy()
    
    fd = FileDetail('cars.csv',
                'csv', 
                '500 bytes', 'cars.csv',
                sub_df
                 )
    
    process = IndividualVariable(fd)
    process.start()
    print(process.full_variables.Variables[0].boxplot_json())