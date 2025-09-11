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
                         "content": ("""Цель:

                                Создание полного и последовательного анализа выбранного художественного произведения с использованием трёх уровней глубины.
                                Входные данные:
                                
                                    Название произведения и автор
                                    Объем текста:
                                        Первый уровень: 2000 ±100 символов.
                                        Второй уровень: 4000 ±200 символов.
                                        Третий уровень: 6000 ±300 символов.
                                    Структура анализа:
                                        Три уровня глубины анализа (фактура → интерпретация → философия и критика).
                                
                                Порядок действий:
                                1. Общая характеристика:
                                
                                    Определение жанра произведения.
                                    Назначение периода написания.
                                    Краткое описание культурного и исторического контекста создания произведения.
                                
                                2. Сюжет и композиция:
                                
                                    Общие линии сюжета.
                                    Композиционная структура (экспозиция, завязка, развитие действия, кульминация, развязка).
                                    Важнейшие эпизоды и их взаимосвязь с общей темой.
                                
                                3. Система персонажей:
                                
                                    Основные действующие лица и их роли.
                                    Второстепенные персонажи и их функциональная нагрузка.
                                    Взаимодействие персонажей и конфликты между ними.
                                
                                4. Идея и проблематика:
                                
                                    Основная тема произведения.
                                    Проблемы, поднимаемые автором (социальные, этические, эстетические).
                                    Средства художественной выразительности (символы, аллюзии, приемы стиля).
                                
                                5. Художественные средства и стиль:
                                
                                    Язык и стиль автора.
                                    Использованные художественные приемы (описания, диалоги, пейзажи, портреты).
                                    Атмосфера произведения и способы её создания.
                                
                                6. Критический анализ:
                                
                                    Историческая ценность произведения.
                                    Место произведения в творчестве автора и литературе в целом.
                                    Актуальность идей и тематики произведения для современности.
                                
                                Итоговый документ:
                                
                                    Ясное изложение ключевой информации о произведении.
                                    Последовательный анализ на заданных уровнях.
                                    Четкие выводы о значимости и влиянии произведения.
                                
                                Дополнительные рекомендации:
                                
                                    Обязательно подкрепляйте выводы цитатами из текста.
                                    При анализе персонажей выделяйте динамику их внутреннего мира.
                                    Обращайте внимание на символику, используемую автором.
                                    Формируйте собственные выводы, избегая шаблонных утверждений.
                                    Избегай разметок HTML и Markdown.""")},

                        {"role": "user", "content": text}
                    ],
                    provider=g4f.Provider.AnyProvider,
                )
                response = ''.join([str(chunk) for chunk in response_generator])
                match = re.search(r"content='(.*?)'", response)
                if match:
                    if match.group(1) == "" or match.group(1) == " " or match.group(1) == "error code: 502":
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


