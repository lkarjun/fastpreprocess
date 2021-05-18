from blueprint import Variable
from essential import *
import tqdm
import pandas as pd
import numpy as np

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
            v = Variable(self.filedetail.obj[i])
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



if __name__ == "__main__":
    df = pd.read_csv('static/dataset/car_testing.csv', delimiter=',')
  
    global fd
    fd = FileDetail('cars.csv',
                'csv', 
                '500 bytes', 'cars.csv',
                df
                 )
    
    process = IndividualVariable(fd)
    process.start()
    print(process.IV.Variables[2].vmostcommon)

    # print(process.IV.Variables[1].vnunique)