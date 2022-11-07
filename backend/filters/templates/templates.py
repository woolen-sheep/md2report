class DocxTemplates:
    # Template of figure number under fugures.
    # Usage: `FIUGURE_NUMBER.format(section_id = s_id, image_id=i_id)`
    FIGURE_NUMBER: str = r"""
                <w:pPr>
                    <w:pStyle w:val="ImageCaption" />
                </w:pPr>
                <w:bookmarkStart w:id="Fig-{section_id}-{image_id}" w:name="图{section_id}-{image_id}" />
                <w:r>
                    <w:t xml:space="preserve">图 </w:t>
                </w:r>
                <w:fldSimple w:instr="STYLEREF 1 \s">
                    <w:r>
                        <w:t>{section_id}</w:t>
                    </w:r>
                </w:fldSimple>
                <w:r>
                    <w:t>-</w:t>
                </w:r>
                <w:fldSimple w:instr="SEQ Figure \* ARABIC ">
                    <w:r>
                        <w:t>{image_id}</w:t>
                    </w:r>
                </w:fldSimple>
                <w:bookmarkEnd w:id="Fig-{section_id}-{image_id}" />
    """
    TABLE_NUMBER: str = r"""
                <w:pPr>
                    <w:pStyle w:val="TableCaption" />
                </w:pPr>
                <w:bookmarkStart w:id="Table-{section_id}-{table_id}" w:name="表{section_id}-{table_id}" />
                <w:r>
                    <w:t xml:space="preserve">表 </w:t>
                </w:r>
                <w:fldSimple w:instr="STYLEREF 1 \s">
                    <w:r>
                        <w:t>{section_id}</w:t>
                    </w:r>
                </w:fldSimple>
                <w:r>
                    <w:t>-</w:t>
                </w:r>
                <w:fldSimple w:instr="SEQ Table \* ARABIC ">
                    <w:r>
                        <w:t>{table_id}</w:t>
                    </w:r>
                </w:fldSimple>
                <w:bookmarkEnd w:id="Table-{section_id}-{table_id}" />
    """

    # `ABSTRACT` is only used to append abstract to the subtitle.
    # Since the subtitle is a meta value, we can't append abstract
    # right behind it. Because subtitle is a paragraph, we can
    # escape the openxml `<w:p>` to append abstract.
    #
    # usage: `ABSTRACT.format(content = "content")`
    ABSTRACT_EN: str = r"""
            </w:p>
            <w:p>
                <w:pPr>
                    <w:pStyle w:val="Abstract" />
                </w:pPr>
                <w:r>
                    <w:t>Abstract</w:t>
                </w:r>
            </w:p>
            <w:p>
                <w:pPr>
                    <w:pStyle w:val="BodyText" />
                </w:pPr>
                <w:r>
                    <w:t>{content}</w:t>
                </w:r>
    """

    ABSTRACT_ZH: str = r"""
            </w:p>
            <w:p>
                <w:pPr>
                    <w:pStyle w:val="Abstract" />
                </w:pPr>
                <w:r>
                    <w:t>摘要</w:t>
                </w:r>
            </w:p>
            <w:p>
                <w:pPr>
                    <w:pStyle w:val="BodyText" />
                </w:pPr>
                <w:r>
                    <w:t>{content}</w:t>
                </w:r>
    """

