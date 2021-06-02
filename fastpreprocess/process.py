from fastpreprocess.operation import *

class FastPreProcess:

    def __init__(self, file: FileDetail) -> None:
        self.file = file
        self.obj = file.obj
        self.copy = file.objcopy
        self.process = IndividualVariable(self.file)
        self.process.start()


    def sample(self, new = False) -> SampleData:
        if new:
            return SampleData(5,
                       self.file.objcopy.sample(5).values.tolist(),
                       self.file.objcopy.columns,
                       len(self.file.objcopy.columns),
                       len(self.file.objcopy))
            
        obj = self.obj
        sample_data = SampleData(5, obj.sample(5).values.tolist(), obj.columns, len(obj.columns), len(obj))
        return sample_data
    
    def quick_stat(self) -> QuickStat:
        try:
            stat = np.round(self.file.obj.describe().values.tolist(), 3).tolist()
            numerical_col = self.file.obj.select_dtypes(exclude = ['object']).columns.to_list()
            zipping = [(variable, data) for variable, data in zip(QuickStat().variables, stat)]
            return QuickStat(stat, numerical_col, zipping)
        except:
            return 0

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


    def get_info(self, column):
        temp = self.copy[column]
        return {'dtype': f'{temp.dtype}', 'count': str(temp.count()), 'unique': str(temp.nunique())}

