from typing import Iterable, List, NamedTuple, Tuple, Type, TypeVar, Union, Set
from pydantic import BaseModel

class FileDetail(BaseModel):
    filename: str
    filetype: str
    filesize: str
    sysfilepath: str
    obj: TypeVar('pandas.core.frame.DataFrame')
    missing: int
    objcopy: TypeVar('pandas.core.frame.DataFrame')

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
    variable: Union[None, List]
    correlation: Union[None, List]
    empty: int = 0
    
    def json(self):
        return  [{'name': i,\
                 'data': [{'x': self.variable[u], 'y': v} for u, v in enumerate(j)]} 
                  for i, j in zip(self.variable, self.correlation)]