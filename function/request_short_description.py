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

    if file_extension.lower() == ".docx":
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
                                     " Для выяснения, что надо вывести - смотрим выходные данные."
                                     "Делай шаг за шагом:"
                                     "1. Проанализируй, есть ли вопросы в тексте"
                                     "2. Если вопросы есть, то собери из текста самое важное для ответов на них."
                                     "Если вопросов нет, то просто укороти текст и переходи к пункту 5"
                                     "3. Если символов для одного ответа больше 300 - укороти текст до 300 символов."
                                     "4. Отвечай ясно и кратко"
                                     "5. Сделай краткий, возможный ответ на вопрос"
                                     "6. Вернись к пункту 1, если ты нашёл что-то новое и они не сходятся с вопросом, то перепроверь ещё раз. Максимальное количество попыток 5, в крайнем случае - выдай текст, как есть"
                                     "Выходные данные: Сами вопросы и ответ на них"
                                     ". Просто краткое описание текста. Не обращай внимание на всякие вещи, по типу spire... И т.д"
                                     "Если нет вопросов, то просто укороти текст для нормального пересказа и понятия смысла. Не используй разметки HTML и Markdown и т.д. Из важного: не расписывай по пунктам, которые написаны, используй выходные данные")},
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


