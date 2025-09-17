import pandas as pd
from pandas import DataFrame


async def convert_xml_to_text(file_name: str) -> DataFrame:
    """
    Конвертирование таблиц в текст
    :param file_name:
    :return:
    """
    text = pd.read_csv(file_name)

    return text
