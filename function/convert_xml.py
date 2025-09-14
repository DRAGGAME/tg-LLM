import pandas as pd

async def convert_xml_to_text(filial_name: str):
    text = pd.read_csv(filial_name)

    return text
