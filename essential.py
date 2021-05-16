from typing import Iterable, List, NamedTuple, Tuple, Type, TypeVar, Union
from pydantic import BaseModel


class VariableDetail(BaseModel):
    vname: str
    missing: str
    vtype: str
    vsummary: Tuple[List, List]
    stat: TypeVar('pandas.core.frame.DataFrame')
    outlier_track: Union[List, None]

    def boxplot_json(self):
        if self.vtype == 'numeric':
            stat = (self.stat.iloc[[3, 4, 5, 6,7]].values).flatten().astype(int).tolist()
            if self.outlier_track is None:
                json = [{'name': self.vname, 'type': 'boxPlot', 'data': [{'x': self.vname, 'y': int(stat)}]}]
                return json
            json = [{'name': self.vname, 'type': 'boxPlot', 'data': [{'x': self.vname, 'y': stat}]}, self.outlier_json()]
            return json
        else: print("Skipping")
    
    def outlier_json(self):
        json = {'name': 'outliers', 
                'type': 'scatter', 
                'data': [{'x': self.vname, 'y': list(set(self.outlier_track))}]}
        return json
        
class IndividualVariables(BaseModel):
    length: int = 0
    Variables: List[Type[VariableDetail]] = []



class FileDetail(NamedTuple):
    filename: str
    filetype: str
    filesize: str
    sysfilepath: str
    obj: object

class SampleData(NamedTuple):
    samplesize: int
    sampledata: List
    columns: List[str]
    number_of_columns: int
    length: int


class QuickStat(NamedTuple):
    stat: List[List[float]] = None
    numerical_col: List = None
    zipped: Tuple[str, List] = None
    variables: List[str] = ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']


class Correlation(BaseModel):
    variable: List[str]
    correlation: List
    
    def json(self):
        return  [{'name': i,\
                 'data': [{'x': self.variable[u], 'y': v} for u, v in enumerate(j)]} 
                  for i, j in zip(self.variable, self.correlation)]