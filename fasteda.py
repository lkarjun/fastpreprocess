import pandas as pd
from essential import SampleData, FileDetail

def file_columns(filedetail: FileDetail) -> SampleData:
    obj = filedetail.obj
    sample_data = SampleData(10, obj.sample(10).values.tolist(), obj.columns, len(obj.columns), len(obj))
    return sample_data


if __name__ == "__main__":
    path = 'static/dataset/bank_data_processed.csv'
    print(list(file_columns(path)[1]))