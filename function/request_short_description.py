import re
import g4f
from aiogram.fsm.context import FSMContext
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


async def request_short_description(file_name: str, level_size: int, level_question: int) -> list:
    client = Client()
    text = f"Размерность текста: {level_size}\nУглублённость вопросов: {level_question}\nТекст: "
    summaries = []

    _, file_extension = os.path.splitext(file_name)
    print("test")
    if file_extension.lower() in [".docx", ".doc", '.odt']:
        try:
            docx = Document()
            docx.LoadFromFile(f"./{file_name}")
            text += docx.GetText()

        except SpireException as e:
            print(f"Ошибка при загрузке DOCX файла: {e}")
            return []
    else:
        print("Поддерживаемые форматы файлов: .docx и .pdf")
        return []

    async def process_chunk(text):
        while True:
            try:
                response_generator = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system",
                         "content": ("Ты - высоко квалифицированный специалист/преподаватель по анализу текста.\n"
                                     "Твоя главная задача - это это подготовить человека к пересказу текста и сдачи теста. "
                                     "Ты предоставляешь данные ученику. По тексту - пойми, какого класса этот ученик в России.\n"
                                     "Текст - литературный"
                               
                                     "Входные данные: Размер сокращённого текста - может быть:"
                                     "1 уровня - 3900 +- 100 символов"
                                     "2 уровня - 6000 +- 200 символов"
                                     "3 уровня - 8000 +- 300 символов"
                               
                                     "Углублённоcть вопросов:"
                                     "1 уровня - 8 вопросов, анализируй текст но не вдавайся сильно в детали. Но обязательны вопросы о самих героях, о основном смысле "
                                     " Для выяснения, что надо вывести - смотрим выходные данные."
                                     "2 уровня - 20 вопросов, анализируй текст, вдавайся в детали. Обязательны вопросы с 1 уровня, о основном теме текста, скрытом смысле."
                                     "3 уровня 30 и более вопросов. Делай всё из второго и первого уровня. Прочитай сначала весь текст. И пойми обязательны вопросы по всему содержанию"
                                     "Остальные входные данные:"
                                     "Текст"

                                     "Инструкция: "
                                     "1. Проанализируй текст, заранее оцени номер класса ученика"
                                     "2. Посмотри размер сокращённого текста, и в зависимости от него и класса ученика - сделай сокращённый текст"
                                     "3. Проанализируй сокращённый текст и составь вопросы в зависимости от углублённости вопросов"
                                     "4. Отвечай на свои вопросы ясно, выдавай ответы максимально близкими к сокращённому тексту"
                                     
                                     "Выходные данные: Сокращённый текст"
                                     
                                     "вопросы текста и ответы на них."
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
                    if match.group(1) == "" or match.group(1) == " ":
                        continue

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


