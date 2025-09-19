import os

import pandas as pd
from pandas import DataFrame


async def convert_xml_to_text(file_name: str) -> DataFrame:
    """
    Конвертирование таблиц в текст
    :param file_name:
    :return:
    """
    text = ""
    _, file_extension = os.path.splitext(file_name)

    if file_extension in [".xml", ".xlsx", ".xlsm", ".ods"]:
        text = pd.read_xml(file_name)
    elif file_extension in [".csv"]:
        text = pd.read_csv(file_name)

    return text
