from typing import List
from docx.document import Document as TDocument
from docx.text.paragraph import Paragraph


def get_paras_by_style_name(doc: TDocument, style_name: str) -> List[Paragraph]:
    res = []
    p: Paragraph
    for p in doc.paragraphs:
        if p.style.name == style_name:
            res.append(p)
    return res
