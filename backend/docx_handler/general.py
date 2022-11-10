from docx import Document
from docx.document import Document as TDocument
from docx.text.paragraph import Paragraph
from docx.shared import Pt


def insert_indent(filename: str, indent_size: float = 24) -> None:
    """
    Insert indent of two Chinese characters to the first line
    of style `Body Text` and `First Paragraph`

    Note: When the font is `宋体 小四`, `indent_size` should
    be 24. If the template uses another font, you should modify
    the `indent_size` by yourself.
    `indent_size` should be `pt_size_of_fone * 2`, and you can
    find pt size here:
        https://en.wikipedia.org/wiki/Traditional_point-size_names
    """
    doc: TDocument = Document(filename)
    styles = ["Body Text", "First Paragraph"]
    indent_size = Pt(indent_size)
    p: Paragraph
    for p in doc.paragraphs:
        if p.style.name not in styles:
            continue
        p.paragraph_format.first_line_indent = indent_size
    doc.save(filename)
