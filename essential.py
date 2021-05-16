from typing import Iterable, List, NamedTuple, Tuple, Type
from pydantic import BaseModel


class VariableDetail(BaseModel):
    vname: str
    missing: str
    vtype: str
    vsummary: Tuple[List, List]
    
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