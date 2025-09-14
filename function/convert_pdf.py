from spire.pdf.common import *
from spire.pdf import *
import re

async def convert_pdf_to_text(file_name: str):

    re_pattern = r"Evaluation Warning : The document was created with Spire.PDF for Python."

    pdf_file = PdfDocument()
    extract_object = PdfTextExtractOptions()
    text = ''

    pdf_file.LoadFromFile(f"{file_name}")

    extract_object.IsExtractAllText = True

    for page_count in range(pdf_file.Pages.Count):
        page = pdf_file.Pages[page_count]
        text_extractor = PdfTextExtractor(page)
        text += text_extractor.ExtractText(extract_object)

    text = re.sub(re_pattern, '', text)

    return text
