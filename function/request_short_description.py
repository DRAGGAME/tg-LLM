import g4f
from g4f import Client
from spire.doc import Document
import asyncio
from g4f.client.stubs import ChatCompletionChoice
import re
async def split_text(text, max_len=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_len
        chunks.append(text[start:end])
        start = end
    return chunks

async def request_short_description(file_name: str) -> str:
    client = Client()
    docx = Document()
    docx.LoadFromFile(f"./{file_name}")
    text = docx.GetText()
    result = ""
    chunks = await split_text(text, max_len=2000)
    summaries = []
    for chunk in chunks:
        try:
            print(chunk)
            response_generator = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Ты - высоко квалифицированный специалист по анализу текста. Твоя главная задача - это укоротить текст документа."
                                                    " Ты предоставляешь данные ученику. По тексту - пойми, какого класса этот ученик"
                                                    "Входные данные: текст документа"
                                                    "выходные данные: краткое описание документа к подготовке к вопросам"
                                                    "Делай шаг за шагом:"
                                                    "1. Проанализируй текст и выдели ключевые моменты"
                                                    "2. По каждому ключевому моменту - анализируй подтемы этого момента"
                                                    "3. По каждой подтеме - укороти текст до состояния, чтобы можно было быстро выучить"
                                                    "4. Собери из подтем - краткое описание момента"
                                                    "5. Собери из кратких описаний - краткое описание всего текста."},
                    {"role": "user", "content": chunk}
                ],
                provider=g4f.Provider.ApiAirforce,
            )
        except g4f.errors.ResponseError as e:
            print(f"Ошибка{e}")
            await asyncio.sleep(60)
            response_generator = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Ты - высоко квалифицированный специалист по анализу текста. Твоя главная задача - это укоротить текст документа."
                                                    " Ты предоставляешь данные ученику. По тексту - пойми, какого класса этот ученик"
                                                    "Входные данные: текст документа"
                                                    "выходные данные: краткое описание документа к подготовке к вопросам"
                                                    "Делай шаг за шагом:"
                                                    "1. Проанализируй текст и выдели ключевые моменты"
                                                    "2. По каждому ключевому моменту - анализируй подтемы этого момента"
                                                    "3. По каждой подтеме - укороти текст до состояния, чтобы можно было быстро выучить"
                                                    "4. Собери из подтем - краткое описание момента"
                                                    "5. Собери из кратких описаний - краткое описание всего текста."},
                    {"role": "user", "content": chunk}
                ],
                provider=g4f.Provider.ApiAirforce,
            )
    for chunk in response_generator:
        result += str(chunk)
    match = re.search(r"content='(.*?)'", result)
    text = match.group(1)
    return text