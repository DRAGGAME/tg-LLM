import os
import pandas as pd
from pandas import DataFrame
import pyexcel_ods3  # Необходимо установить библиотеку pip install pyexcel-ods3


def convert_file_to_dataframe(file_name: str) -> DataFrame:
    """
    Конвертирует файл XML, XLSX, ODS или CSV в объект Pandas DataFrame

    :param file_name: Имя файла (например, 'data.csv' или 'report.xlsx')
    :return:
    """
    _, file_extension = os.path.splitext(file_name)

    if file_extension.lower() in ['.xml', '.xlsx']:
        df = pd.read_excel(file_name)
    elif file_extension.lower() == '.csv':
        df = pd.read_csv(file_name, encoding='utf-8')
    elif file_extension.lower() == '.ods':
        data = pyexcel_ods3.get_data(file_name)
        sheet_name = list(data.keys())[0]
        df = pd.DataFrame(data[sheet_name])
    else:
        raise ValueError(f"Файл '{file_name}' имеет неподдерживаемое расширение.")

    return df