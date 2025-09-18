import pandas as pd
from logger import logger


async def convert_xml_to_text(file_name: str) -> str:
    """
    Конвертация CSV в чистый текст (строку).
    Автоматически определяет разделитель и кодировку.
    """
    try:
        encodings_to_try = ["utf-8-sig", "utf-8", "cp1251", "latin1"]
        last_error = None

        for enc in encodings_to_try:
            try:
                df = pd.read_csv(file_name, sep=None, engine="python", encoding=enc)
                if not df.empty:
                    # Конвертируем в текст
                    text = df.to_string(index=False)
                    return text
            except Exception as e:
                last_error = e
                logger.error(f"Ошибка чтения CSV с кодировкой {enc}: {e}")
                continue

        raise ValueError(f"Не удалось прочитать CSV-файл. Последняя ошибка: {last_error}")

    except Exception as e:
        logger.error(f"Критическая ошибка при обработке CSV {file_name}: {e}")
        return ""
