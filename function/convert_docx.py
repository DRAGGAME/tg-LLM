import re

from spire.doc import Document


async def convert_docx_to_text(file_name: str) -> str:
    """
    Конвертирование файла-документа в текст.
    Предварительно убирается строка от библиотеки spire
    Работает только с текстом

    :param file_name:
    :return:
    """
    text = ""
    re_pattern = r"Evaluation Warning : The document was created with Spire.Doc for Python."

    docx = Document()
    docx.LoadFromFile(f"./{file_name}")
    text += docx.GetText()
    text = re.sub(re_pattern, '', text)

    return text
