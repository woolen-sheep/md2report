from typing import Callable, Dict
from docx_handler.hust import process_hust_docx
from docx_handler.general import insert_indent

handler_map: Dict[str, Callable] = {
    "HUST": process_hust_docx,
    "first_line_indent": insert_indent,
}
