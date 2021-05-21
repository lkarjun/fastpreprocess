from operation import *

class FastEda:

    def __init__(self, file: FileDetail) -> None:
        self.file = file
        self.obj = file.obj
        self.process = IndividualVariable(self.file)
        self.process.start()


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

