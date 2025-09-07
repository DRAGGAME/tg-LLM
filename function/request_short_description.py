from g4f import Client
from spire.doc import *
from spire.doc.common import *

async def request_short_description(file_name: str) -> str:
    client = Client()
    docx = Document()
    docx.LoadFromFile(f"./{file_name}")
    text = docx.GetText()
    print(text)
    response = client.chat.completions.create(
        model="gpt-4",

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

                  {"role": f"Привет, опиши мне этот документ {text}"}],
        timeout=15
    )

    return response.choices[0].message.content