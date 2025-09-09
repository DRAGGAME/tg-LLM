import re
import g4f
from g4f import Client
from spire.doc import Document, SpireException
from spire.pdf import PdfDocument, FileFormat
import asyncio
import os


async def split_text(text, max_len=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_len
        chunks.append(text[start:end])
        start = end
    return chunks


async def request_short_description(file_name: str) -> list:
    client = Client()
    text = ""

    _, file_extension = os.path.splitext(file_name)

    if file_extension.lower() == ".docx":
        try:
            docx = Document()
            docx.LoadFromFile(f"./{file_name}")
            text = docx.GetText()
        except SpireException as e:
            print(f"Ошибка при загрузке DOCX файла: {e}")
            return []

    elif file_extension.lower() == ".pdf":
        try:
            pdf = PdfDocument()
            pdf.LoadFromFile(f"./{file_name}")
            for page in range(pdf.Pages.Count):
                text += pdf.Pages[page].ExtractText(True)
        except Exception as e:
            print(f"Ошибка при загрузке PDF файла: {e}")
            return []

    else:
        print("Поддерживаемые форматы файлов: .docx и .pdf")
        return []

    chunks = await split_text(text, max_len=2000)
    summaries = []

    async def process_chunk(chunk):
        while True:
            try:
                response_generator = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system",
                         "content": ("Ты - высоко квалифицированный специалист по анализу текста. "
                                     "Твоя главная задача - это укоротить текст документа. "
                                     "Ты предоставляешь данные ученику. По тексту - пойми, какого класса этот ученик."
                                     "Входные данные: текст документа"
                                     "Выходные данные: краткое описание документа к подготовке к вопросам. Используй разметку HTML"
                                     "Делай шаг за шагом:"
                                     "1. Проанализируй текст и выдели ключевые моменты."
                                     "2. По каждому ключевому моменту - анализируй подтемы этого момента."
                                     "3. По каждой подтеме - укороти текст до состояния, чтобы можно было быстро выучить."
                                     "4. Собери из подтем - краткое описание момента."
                                     "5. Собери из кратких описаний - краткое описание всего текста.")},
                        {"role": "user", "content": chunk}
                    ],
                    provider=g4f.Provider.AnyProvider,
                )
                response = ''.join([str(chunk) for chunk in response_generator])
                match = re.search(r"content='(.*?)'", response)
                if match:
                    return match.group(1)
            except g4f.errors.ResponseError as e:
                print(f"Ошибка: {e}")
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")
                await asyncio.sleep(10)

    for chunk in chunks:
        summary = await process_chunk(chunk)
        if summary:
            summaries.append(summary)

    full_summary = ' '.join(summaries)
    full_summary = full_summary.replace("\\n", "\n")
    final_chunks = await split_text(full_summary, max_len=4096)
    return final_chunks


