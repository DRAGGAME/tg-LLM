import re
import g4f
from g4f import Client
from spire.doc import Document, SpireException
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

    if file_extension.lower() in [".docx", ".odt", ".doc"]:
        try:
            docx = Document()
            docx.LoadFromFile(f"./{file_name}")
            text = docx.GetText()
        except SpireException as e:
            print(f"Ошибка при загрузке DOCX файла: {e}")
            return []
    else:
        print("Поддерживаемые форматы файлов: .docx и .pdf")
        return []

    chunks = await split_text(text, max_len=2000)
    summaries = []

    async def process_chunk(text):
        while True:
            try:
                response_generator = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system",
                         "content": ("Ты - высоко квалифицированный специалист по анализу текста. "
                                     "Твоя главная задача - это это подготовить человека к вопросам по тексту и дальнейшему его пересказу."
                                     "Ты предоставляешь данные ученику. По тексту - пойми, какого класса этот ученик в России."
                                     "Входные данные: текст документа"
                                     " Для выяснения, что надо вывести - смотрим выходные данные."
                                     "Инструкция: "
                                     "1. Сделай краткий текст с сохранением основного содержания."
                                     "2. Ответь на вопросы, которые есть в тексте и переходи к 4 пункту."
                                     "3. Если вопросов нет - проанализируй текст и создай вопросы для ученика того класса"
                                     "4. Отвечай на свои вопросы ясно и кратко"
                                     "Выходные данные: Сокращённый текст"
                                     ", вопросы текста и ответы на них."
                                     "Не обращай внимание на всякие вещи, по типу spire... И т.д"
                                     "Не используй разметки"
                                     " HTML и Markdown и т.д. Из важного: не расписывай по пунктам, которые написаны, используй выходные данные")},
                        {"role": "user", "content": text}
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

    # for chunk in chunks:
    summary = await process_chunk(text)
    if summary:
        summaries.append(summary)

    full_summary = ' '.join(summaries)
    full_summary = full_summary.replace("\\n", "\n")
    final_chunks = await split_text(full_summary, max_len=4096)
    return final_chunks


