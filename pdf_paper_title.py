from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTAnno


def get_paper_title(filename):
    title = ""

    # 标题通常在第一页，故只循环一次
    for page_layout in extract_pages(filename):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if text_line.x1 - text_line.x0 < 30:
                        continue
                    text_line_str = ""
                    is_title = False
                    for character in text_line:
                        if isinstance(character, LTChar):
                            text = character.get_text()
                            font_size = character.size
                            # 经验值
                            if font_size > 14.3:
                                is_title = True
                            text_line_str += text
                        elif isinstance(character, LTAnno):
                            text = character._text
                            text_line_str += text
                    if is_title:
                        if len(title) == 0:
                            title = text_line_str.strip("\n")
                        else:
                            title = "{} {}".format(title, text_line_str).strip("\n")
        break

    return title.strip()


if __name__ == '__main__':
    filename = "data/arxiv.pdf"
    title = get_paper_title(filename)
    print("title:\n{}".format(title))