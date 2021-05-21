import tqdm
import pandas as pd
import numpy as np
from pandas.api.types import is_bool_dtype, is_numeric_dtype
from essential import *

class NumericDetail(BaseModel):
    data: TypeVar('pandas.core.series.Series')
    vname: str
    vmissing: Union[Tuple[int, float], None]
    vtype: str
    vsummary: Tuple[List, List]
    vstat: TypeVar('pandas.core.frame.DataFrame')
    voutlier_track: Union[List, None]
    vhtmlid: Tuple[str, str]
    
    def boxplot_json(self):
        stat = (self.vstat.iloc[[3, 4, 5, 6,7]].values).flatten().astype(int).tolist()
        if self.voutlier_track is None:
            json = [{'name': self.vname, 'type': 'boxPlot', 'data': [{'x': self.vname, 'y': int(stat)}]}]
            return json
        json = [{'name': self.vname, 'type': 'boxPlot', 'data': [{'x': self.vname, 'y': stat}]}, self.outlier_json()]
        return json
    
    def outlier_json(self):
        json = {'name': 'outliers', 
                'type': 'scatter', 
                'data': [{'x': self.vname, 'y': list(set(self.voutlier_track))}]}
        return json

    def distribution_json(self):
        hist = np.histogram(self.data.dropna().values)
        counter = hist[0].astype(int).tolist()
        categ = np.round(hist[1], 2).astype(str).tolist()
        json = {'data': counter, 'categories': categ}
        return [json]


class CategoricalDetail(BaseModel):
    vname: str
    vmissing: Union[Tuple[int, float], None]
    vtype: str
    vsummary: Tuple[List, List]
    vstat: TypeVar('pandas.core.frame.DataFrame')
    vhtmlid: Tuple[str, str]
    vnunique: int
    vnuniquevalues: Set[str]
    vmostcommon: Tuple[List, List, List]

    def barplot_json(self):
        return  {'categories': self.vmostcommon[0], 'data': self.vmostcommon[2]}


class IndividualVariables(BaseModel):
    TotalNumeric: int = 0
    TotalCategorical: int = 0
    Length: int = 0
    Variables: List[Union[NumericDetail, CategoricalDetail]] = []


class IndividualVariable():

    def __init__(self, filedetail: FileDetail):
        self.filedetail = filedetail
        self.data = filedetail.obj
        self.IV = IndividualVariables()
    
    def outlier(self, v, i):
        df = self.data
        q1q2 = v.statistics.iloc[[4,6]].values.flatten()
        IQR = q1q2[1] - q1q2[0]
        outlier = df[i][(df[i] < (q1q2[0] - 1.5 * IQR)) |(df[i] > (q1q2[1] + 1.5 * IQR))].values
        return (outlier.astype(int)).tolist()
        
    def start(self):
        for i in tqdm.tqdm(self.filedetail.obj.columns, desc="Univariate Analysing"):
            v = Bivariate(self.filedetail.obj[i])
            if v.var_type == 'numeric':
                self.IV.TotalNumeric += 1
                var = NumericDetail(
                            data = self.filedetail.obj[i],
                            vname=i,
                            vmissing=v.missing,
                            vtype=v.var_type,
                            vsummary=(v.statistics.index.to_list(), v.statistics.values.flatten().tolist()),
                            vstat=v.statistics,
                            voutlier_track=self.outlier(v, i),
                            vhtmlid=(f'#var{self.IV.Length}', f'var{self.IV.Length}')
                    )
                
            if v.var_type == 'categorical':
                self.IV.TotalCategorical += 1
                var = CategoricalDetail(
                            vname=i,
                            vmissing=v.missing,
                            vtype=v.var_type,
                            vsummary=(v.statistics.index.to_list(),  v.statistics.values.flatten().tolist()),
                            vstat=v.statistics,
                            vhtmlid=(f'#var{self.IV.Length}', f'var{self.IV.Length}'),
                            vnunique = v.num_unique,
                            vnuniquevalues = v.unique,
                            vmostcommon = v.most_common_items
                    )
            
            self.IV.Variables.append(var)
            self.IV.Length += 1

        assert self.IV.Length == len(self.data.columns), "Length counter value and total number of columns is different"




class Bivariate:

    def __init__(self, data):
        self.data = data
        self.var_type = self.variable_type()
        self.statistics = self.summary()
        self.num_unique = self.data.nunique()
        self.unique = set(self.data.unique())
        self.missing = self.missing_value()


    def variable_type(self):
        if is_numeric_dtype(self.data) and not is_bool_dtype(self.data):
            # Only int and float types
            return 'numeric'
        else:
            # Handle bool, string, datetime, etc as categorical
            self.data = self.data.astype('category')
            return 'categorical'

    def summary(self):

        if self.var_type == 'numeric':
            return self.numerical_summary()
        elif self.var_type == 'categorical':
            return self.categorical_summary()

    def numerical_summary(self):

        summary = self.data.describe()
        summary.index = [
            'Number of observations', 'Average', 'Standard Deviation',
            'Minimum', 'Lower Quartile', 'Median', 'Upper Quartile', 'Maximum'
        ]
        summary['Skewness'] = self.data.skew()
        summary['Kurtosis'] = self.data.kurt()
        return summary.round(7).to_frame()

    def categorical_summary(self):

        summary = self.data.describe()[['count', 'unique', 'top']]
        summary.index = ['Number of observations', 'Unique values',
                         'Mode (Highest occurring value)']

        most_common_items = self.data.value_counts().head()
        n = len(self.data)
        var = most_common_items.index.to_list()
        count = most_common_items.values.tolist()
        percentage = most_common_items.apply(lambda x: f'{x / n:.2%}').values.tolist()
        self.most_common_items = \
            var, percentage, count

        return summary.to_frame()

    def missing_value(self):

        missing_values = self.data.isna().sum()
        if missing_values == 0:
            return None
        else:
            return missing_values, round(missing_values / len(self.data), 3)

    
