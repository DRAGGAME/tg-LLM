import re
import g4f
from g4f import Client
import asyncio
import os

from function.convert_docx import convert_docx_to_text
from function.convert_pdf import convert_pdf_to_text
from function.convert_pptx import convert_pptx_to_text


async def split_text(text, max_len=50):
    """
    Разбитие текста
    :param text:
    :param max_len:
    :return:
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_len
        chunks.append(text[start:end])
        start = end
    return chunks


async def request_short_description(file_name: str, level: int, level_question: int) -> list:
    """
    Работа с ИИ
    Отправляется запрос на получение текста
    Отправление текста к ИИ
    :param file_name:
    :param level:
    :param level_question:
    :return:
    """
    client = Client()
    text = f"Уровни глубины,: {level}\nУглублённость вопросов: {level_question}\nТекст: "
    summaries = []

    _, file_extension = os.path.splitext(file_name)
    if file_extension.lower() in [".docx", ".doc", '.odt']:
        text += await convert_docx_to_text(file_name)

    elif file_extension.lower() in [".pdf"]:
        text += await convert_pdf_to_text(file_name)

    elif file_extension.lower() in [".pptx", ".ppt", ".odp"]:
        text += await convert_pptx_to_text(file_name)

    else:

        return []

    async def process_chunk(text):
        while True:
            try:
                system_prompt = """
                    Ты выступаешь в роли профессионального аналитика текста. 
                    Перед тобой поставлена задача детально проанализировать представленный текст, 
                    учитывая его типологию и глубину изложенного материала. Твой итоговый отчет должен быть четким,
                    структурированным и легким для восприятия.

                    Инструкция по проведению анализа:
                    
                    Шаг 1. Определение типа текста
                    
                    Выделяются три возможных варианта:
                    
                    - Научный или учебник (например, математика, физика, химия).
                    - Есстественно-научный (например, география, история, философия).
                    - Художественный жанр (романы, рассказы, пьесы).
                    
                    При определении типа важно учитывать специфику тематики и стиля подачи материала.
                    
                    Шаг 2. Выбор соответствующей схемы анализа
                    
                    Для научного/учебного текста:
                    
                    Анализ проводится по следующим уровням:
                    
                    - Подготовка: Цель, назначение и практическое значение текста.
                    - Объяснение материала: Краткое изложение ключевых понятий, формул, выводов.
                    - Закрепление: Дополнительные задания и контрольные вопросы.
                    
                    Для естественно-научного текста:
                    
                    Необходимо осветить следующие моменты:
                    
                    - Введение: Повторение пройденного материала и постановка проблемных вопросов.
                    - Объяснение: Детальное рассмотрение каждой ключевой темы и связанной проблематики.
                    - Закрепление: Проверочные вопросы и упражнения для закрепления материала.
                    
                    Для художественного текста:
                    
                    Проведение комплексного анализа включает:
                    
                    - Общая характеристика: История написания, жанровая принадлежность, культурный фон.
                    - Сюжет и композиция: Разбор сюжетных линий, повествование, композиционные особенности.
                    - Персонажи: Рассмотрение главных героев, характеров, конфликтов.
                    - Проблематика: Выявление центральных тем, этических аспектов произведения.
                    - Средства выразительности: Использование стилистических приемов, символов, образов.
                    - Критический разбор: Оценка актуальности и значения произведения.
                    
                    Шаг 3. Глубина проработки
                    
                    Для каждого типа текста предусмотрена трехступенчатая система детализации:
                    
                    - Базовая глубина: Общее ознакомительное содержание.
                    - Расширенная глубина: Углубленные объяснения, дополнительные подробности.
                    - Профессиональная глубина: Аналитические выкладки, критические оценки и возможные приложения материалов.
                    
                    Также предусмотрены аналогичные уровни для формулировки проверочных вопросов:
                    
                    - Базовые вопросы: Прямой пересказ фактов и содержимого.
                    - Расширенные вопросы: Понимание структуры, взаимосвязей элементов.
                    - Профессиональные вопросы: Провоцируют глубокое осмысление, выявление собственной точки зрения.
                    
                    Шаг 4. Финальный отчет
                    
                    Итоговый документ обязательно должен включать:
                    
                    - Четкий последовательный анализ всего текста.
                    - Необходимые цитаты и выдержки из исходника.
                    - Логичные заключения и обобщения.
                    - Набор проверочных заданий и соответствующих решений.
                    - Отсутствие ненужных декоративных элементов оформления.
                    
                    Таким образом, твоя цель — создать детальный и исчерпывающий анализ текста согласно указанным критериям.
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

    summary = await process_chunk(text)
    if summary:
        summaries.append(summary)

    full_summary = ' '.join(summaries)
    full_summary = full_summary.replace("\\n", "\n")
    full_summary = full_summary.replace("**", "")

    final_chunks = await split_text(full_summary, max_len=4096)
    return final_chunks
