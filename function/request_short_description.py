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
                         "content": ("""Цель: Подготовить материал для эффективного изучения и успешного прохождения экзамена по литературе.
                                    Входные Данные
                                    
                                        Исходный текст: Роман Льва Толстого "Война и мир".
                                            Объем текста:
                                                Уровень 1: ~3900 символов ±100.
                                                Уровень 2: ~6000 символов ±200.
                                                Уровень 3: ~8000 символов ±300.
                                            Глубина анализа:
                                                Уровень 1: Основные герои, сюжет, общий смысл.
                                                Уровень 2: Подробности сюжета, мотивы персонажей, скрытые смыслы.
                                                Уровень 3: Полный анализ содержания, включая философско-исторический подтекст.
                                        Класс учащегося: Оцените уровень текста и ориентировочный класс школьника в России (например, 9-й, 10-й классы).
                                    
                                    Инструкция
                                    
                                        Анализ текста: Определите объём и глубину изложения материала, учитывая указанные уровни.
                                        Сокращение текста: Создайте сокращённую версию исходного текста согласно выбранному уровню и классу учащихся.
                                        Формулирование вопросов: Составьте список вопросов для проверки усвоения материала. Количество вопросов:
                                            Уровень 1: 8 вопросов.
                                            Уровень 2: 20 вопросов.
                                            Уровень 3: 30+ вопросов.
                                        Ответы на вопросы: Ответьте на сформулированные вопросы ясно и лаконично, основываясь исключительно на содержании сокращённого текста.
                                    
                                    Выходные Данные
                                    
                                        Сокращённая версия текста.
                                        Список вопросов по тексту.
                                        Ответы на вопросы.
                                    
                                    Примечания
                                    
                                        Форматируйте ответы последовательно и понятно, избегая сложной структуры вроде маркировки списков.
                                        Исключите использование HTML-разметки и Markdown.
                                        Максимально упрощайте формулировки и делайте их удобными для восприятия учениками соответствующего уровня.""")},

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


