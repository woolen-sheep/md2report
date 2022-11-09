import logging
import yaml
from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class ConfigLoadFailed(Exception):
    pass


class ConfigParseFailed(Exception):
    pass


class TemplateConfig(BaseModel):
    pandoc_filters: List[str] = []
    docx_handlers: List[str] = []
    reference: str = ""


class Config(BaseModel):
    config: str = Field(default="", description="Path to the config file.")
    highlight: bool = Field(
        default=True, description="Enable the highlight of code blocks."
    )
    output: str = Field(default="output.docx", description="Output filename.")
    input: str = Field(description="Input filename.")
    template: str = Field(default="HUST", description="Template config name.")
    templates: Dict[str, TemplateConfig] = {}
    indent_font_size: float = Field(default=12.0, description="First line indent font size in pt.")
    indent_font_num: int = Field(default=2, description="First line indent num.")

class ServerConfig(BaseModel):
    cache_path:str = "/tmp/md2report"


def load_config(args: Dict, filename: str = "config/config.yaml"):
    try:
        with open(filename) as stream:
            config = yaml.safe_load(stream=stream)
            config.update(args)
            return Config.parse_obj(config)
    except Exception as e:
        raise ConfigLoadFailed

def load_server_config(filename: str = "config/server_config.yaml"):
    try:
        with open(filename) as stream:
            config = yaml.safe_load(stream=stream)
            return ServerConfig.parse_obj(config)
    except Exception as e:
        logging.error("load server onfig failed")
        raise ConfigLoadFailed

server_config = load_server_config()
