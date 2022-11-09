from typing import List
from docx import Document
from docx.document import Document as TDocument
from docx.text.paragraph import Paragraph
from docx.shared import Pt

def get_paras_by_style_name(doc: TDocument, style_name: str) -> List[Paragraph]:
    res = []
    p: Paragraph
    for p in doc.paragraphs:
        if p.style.name == style_name:
            res.append(p)
    return res

def insert_indent(filename: str, indent_font_size: float, indent_font_num: int):
    if indent_font_num <= 0:
        return
    doc: TDocument = Document(filename)
    styles = ['Body Text', 'First Paragraph']
    indent_size = Pt(indent_font_size) * indent_font_num
    for s in styles:
        paras = get_paras_by_style_name(doc, s)
        for p in paras:
            p.paragraph_format.first_line_indent = indent_size
    doc.save(filename)