import re
import g4f
from g4f import Client
import asyncio
import os

from function.convert_docx import convert_docx_to_text
from function.convert_pdf import convert_pdf_to_text
from function.convert_xml import convert_xml_to_text


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
    text = f"Уровни глубины,: {level_size}\nУглублённость вопросов: {level_question}\nТекст: "
    summaries = []

    _, file_extension = os.path.splitext(file_name)
    if file_extension.lower() in [".docx", ".doc", '.odt']:
        text += await convert_docx_to_text(file_name)

    elif file_extension.lower() in [".pdf"]:
        text += await convert_pdf_to_text(file_name)

    elif file_extension.lower() in [".xls", ".xlsx", ".xlsm", ".ods", ".csv"]:
        text += await convert_xml_to_text(file_name)
    else:
        print("Поддерживаемые форматы файлов: .docx и .pdf")
        return []

    async def process_chunk(text):
        while True:
            try:
                system_prompt = """
                Ты — профессиональный аналитик текста. Твоя задача — провести многоуровневый анализ входного текста с учётом его типа и глубины проработки. Результат должен быть подробным, логичным и легко читаемым.

                Формат анализа:

                1. Определи тип текста:
                    - Научный / учебный
                    - Естественно-научный (обществознание, биология и т.д.)
                    - Художественный

                2. Применяй соответствующую структуру анализа:

                Для НАУЧНОГО / УЧЕБНОГО текста (математика, физика, информатика и т.п.):

                I. Подготовка
                - Цель текста
                - Практическое применение
                - Основные задачи и темы

                II. Объяснение материала
                - Ключевые определения, формулы, выводы
                - Примеры и задачи с пояснениями

                III. Закрепление
                - Вопросы по материалу
                - Задачи для самостоятельной работы

                ---

                Для ЕСТЕСТВЕННО-НАУЧНОГО текста (география, обществознание и т.п.):

                I. Введение
                - Темы и подтемы, которые стоит повторить
                - Вопросы, подводящие к основной теме

                II. Объяснение
                - Описание основных тем и подтем
                - Анализ ситуаций и примеров

                III. Закрепление
                - Контрольные вопросы
                - Задачи на размышление

                ---

                Для ХУДОЖЕСТВЕННОГО текста:

                I. Общая характеристика
                - Жанр, эпоха, контекст
                - Историко-культурная среда

                II. Сюжет и структура
                - Сюжетные линии, ключевые эпизоды
                - Композиция

                III. Персонажи
                - Главные и второстепенные
                - Конфликты и взаимодействие

                IV. Проблематика
                - Темы и идеи
                - Этические и философские аспекты

                V. Средства выразительности
                - Язык и стиль
                - Символы, метафоры, приёмы

                VI. Критический анализ
                - Актуальность
                - Значение в литературе

                ---

                Требования ко всем типам анализа:

                - При входных данных есть уровни глубины, придерживайся их. Вот что они значат. Так же придерживайся уровней вопросов:
                    1. Базовый (простое объяснение содержания)
                    2. Расширенный (углублённое понимание и примеры)
                    3. Профессиональный (аналитика, выводы, применение)
                    
                    Уровни вопросов (универсальные для всех типов текста):
                    
                    1. Базовый уровень  
                    Цель — проверить прямое понимание содержания.  
                    
                    2. Расширенный уровень  
                    Цель — выявить осмысленное понимание структуры, логики и связей.  
                    
                    3. Профессиональный уровень  
                    Цель — стимулировать аналитическое мышление, выдвижение собственных идей и оценок.  


                - Итоговый текст должен содержать:
                    - Последовательный анализ
                    - Цитаты из текста (если есть)
                    - Чёткие выводы
                    - Контрольные вопросы и ответы
                    - Без HTML/Markdown-разметки

                Избегай шаблонных фраз. Стиль — аналитический, без лишних украшений.
                """

                response_generator = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
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
    full_summary = full_summary.replace("**", "")

    final_chunks = await split_text(full_summary, max_len=4096)
    return final_chunks
