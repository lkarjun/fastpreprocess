from essential import *
import numpy as np
import pandas as pd

class FastEda:

    def __init__(self, file: FileDetail) -> None:
        self.file = file
        self.obj = file.obj

    def file_columns(self) -> SampleData:
        obj = self.obj
        sample_data = SampleData(5, obj.sample(5).values.tolist(), obj.columns, len(obj.columns), len(obj))
        return sample_data
    
    def quick_stat(self) -> QuickStat:
        stat = np.round(self.file.obj.describe().values.tolist(), 3).tolist()
        numerical_col = self.file.obj.select_dtypes(exclude = ['object']).columns.to_list()
        zipping = [(variable, data) for variable, data in zip(QuickStat().variables, stat)]
        return QuickStat(stat, numerical_col, zipping)

    def correlation(self) -> Correlation:
        
        # -------------------------------------------Debuging----------------------------------------
        corr = self.obj.corr()
        if len(corr) > 1:
            index = [k for i, k in zip(~corr.iloc[:1].isna().values.flatten(), corr.columns.values) if i]
            corr = corr[index].dropna()
            corr = np.round(corr.values, 3).tolist()
            return Correlation(variable = index, correlation = corr, empty=1) if len(index) > 1 \
                   else Correlation(variable = None, correlation = None, empty=0)
        # -------------------------------------------Debuging----------------------------------------
        
        return Correlation(variable = None,
                           correlation = None,
                           empty=0
                    )


if __name__ == "__main__":
    df = pd.read_csv('static/dataset/cardio_test.csv')
    df = df[[' year', ' brand']]
    fd = fd = FileDetail(filename ='cars.csv',
                     filetype='csv', 
                     filesize='500 bytes', 
                     sysfilepath='cars.csv',
                     obj=df,
                     missing=df.isna().sum().values.sum())
    
    fasteda = FastEda(fd)
    # print(fasteda.correlation().json())
    print(fasteda.correlation())
    # process = IndividualVariable(fd)
    # process.start()
    # print(process.full_variables.length)
