from typing import Callable, Dict
from docx_handler.hust import process_hust_docx

handler_map: Dict[str, Callable] = {"HUST": process_hust_docx}

