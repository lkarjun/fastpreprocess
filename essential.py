from typing import List, NamedTuple, Tuple


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
    zipped: Tuple[str, List] = None
    variables: List[str] = ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']