from templates.templates import DocxTemplates
from typing import Optional, cast, List
import panflute as pf

IMAGE_CAPITAL_TEMPLATE = "{} "


class Index:
    """
    For storing the section number, image number and table number
    of the document.
    """

    image: int = 0
    table: int = 0
    number: List[int] = [0, 0, 0]

    @classmethod
    def add(cls, level: int) -> None:
        """
        Add the index by levelself.

        Note: only the first 3 levels will be stored (i.e. H1 to H3).
        """
        if level >= 4:
            return
        level -= 1
        cls.number[level] += 1
        if level == 1:
            cls.image = 0
            cls.table = 0

    @classmethod
    def to_str(cls) -> str:
        res = ""
        for n in cls.number:
            if n != 0:
                res += f"{n}."
        return res

    @classmethod
    def get_section_id(cls, level: int):
        if level >= 4:
            return 0
        return cls.number[level - 1]

    @classmethod
    def image_index(cls) -> str:
        return cls.to_str() + f"{cls.image}"

    @classmethod
    def table_index(cls) -> str:
        return cls.to_str() + f"{cls.table}"


class DocState:
    # Table titles are placed in front of the table.
    # So we need to store it here.
    table_title: str = ""
    # Chinese abstract
    abstract_zh: str = ""
    # English abstract
    abstract_en: str = ""


def add_image_capition(elem, doc) -> Optional[List[pf.Inline]]:
    """
    Add image number with section number to image caption.
    """
    if type(elem) == pf.Str:
        elem_str: pf.Str = cast(pf.Str, elem)
        # Insert the image number with template
        number = pf.RawInline(
            DocxTemplates.FIGURE_NUMBER.format(
                section_id=Index.get_section_id(level=1), image_id=Index.image
            ),
            format="openxml",
        )
        return [
            number,
            pf.Str(" " + elem_str.text),
        ]


def append_abstract(elem, doc):
    """
    Append abstract after the subtitle.
    """
    if type(elem) == pf.Str:
        res = [elem]
        abstract_zh_str = doc.get_metadata("abstract_zh",None)
        if abstract_zh_str :
            abstract_zh = pf.RawInline(
                DocxTemplates.ABSTRACT_ZH.format(content=abstract_zh_str),
                format="openxml",
            )
            res.append(abstract_zh)
        abstract_en_str = doc.get_metadata("abstract_en",None)
        if abstract_en_str != "":
            abstract_en = pf.RawInline(
                DocxTemplates.ABSTRACT_EN.format(content=abstract_en_str),
                format="openxml",
            )
            res.append(abstract_en)

        return res


def process_report(elem, doc):
    """
    Traverse the JSON AST provided by pandoc, and apply
    modifications such as styles, captions, reference, etc.
    """
    if type(elem) == pf.MetaMap:
        meta: pf.MetaMap = cast(pf.MetaMap, elem)
        meta.content["subtitle"].walk(append_abstract)  # type: ignore
    elif type(elem) == pf.Image:
        img: pf.Image = cast(pf.Image, elem)
        Index.image += 1
        img.walk(add_image_capition)
        return img
    elif type(elem) == pf.Table:
        table: pf.Table = cast(pf.Table, elem)
        Index.table += 1
        number = pf.RawInline(
            DocxTemplates.TABLE_NUMBER.format(
                section_id=Index.get_section_id(level=1), table_id=Index.table
            ),
            format="openxml",
        )
        table.caption = pf.Caption(pf.Para(number, pf.Str(DocState.table_title)))
        DocState.table_title = ""
        return table
    elif type(elem) == pf.Para:
        elem_str: pf.Para = cast(pf.Para, elem)
        content = pf.stringify(elem_str)
        # store the table caption and remove it from the doc.
        if content.startswith("#table "):
            DocState.table_title = content[7:]
            return pf.Para()
    elif type(elem) == pf.Header:
        header: pf.Header = cast(pf.Header, elem)
        Index.add(header.level)


if __name__ == "__main__":
    pf.toJSONFilter(process_report)
