import asyncio

from spire.presentation import Presentation

async def convert_pptx_to_text(file_name: str) -> str:
    """
    Преобразование презентаций в текст
    Работает только с текстом
    :param file_name:
    :return:
    """
    presentation = Presentation()
    presentation.LoadFromFile(file_name)
    text = ""
    for slide in presentation.Slides:
        if slide.GetAllTextFrame() is not None:
            for text_slide in slide.GetAllTextFrame():
                if text_slide:
                    text_slide = text_slide
                else:
                    text_slide = "Нет"

                text += f"Слайд: {slide.SlideNumber} - {text_slide}\n"
    print(text)
    return text
