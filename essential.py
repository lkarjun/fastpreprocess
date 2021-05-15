from typing import List, NamedTuple


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
