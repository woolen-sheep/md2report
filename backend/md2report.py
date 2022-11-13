from pydantic import BaseModel
from config.config import Config, load_config
import yaml
import subprocess
import configargparse
import pathlib
import os
from docx_handler import handler_map


class Metadata(BaseModel):
    title: str = "主标题"
    subtitle: str = "副标题"
    abstract_zh: str = ""
    abstract_en: str = ""
    author: str = ""
    school: str = ""
    major: str = ""


def validate_metadata(filename: str):
    reading_meta = False
    meta_str = ""
    data = ""
    with open(filename, "r") as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            l = l.strip()
            if l == "":
                continue
            if not reading_meta and l != "---":
                data = "".join(lines[i:])
                break
            if l == "---":
                if not reading_meta:
                    reading_meta = True
                    continue
                else:
                    data = "".join(lines[i + 1 :])
                    break
            meta_str += l + "\n"
    if meta_str == "":
        meta = Metadata()
    else:
        meta = Metadata.parse_obj(yaml.safe_load(meta_str))
    meta_str = yaml.safe_dump(meta.dict())
    filename += ".validated.md"
    with open(filename, "w") as f:
        f.write("\n".join(["---", meta_str, "---\n"]))

        f.write(data)
    return filename


def convert_md_to_docx(conf: Config):
    filter_path: pathlib.Path = pathlib.Path(__file__).parent.resolve() / "filters"
    reference_path: pathlib.Path = (
        pathlib.Path(__file__).parent.resolve() / "reference-docs"
    )
    if conf.output.startswith("/"):
        output_path: pathlib.Path = pathlib.Path(conf.output).resolve()
    else:
        output_path: pathlib.Path = pathlib.Path(os.getcwd()).resolve() / conf.output
    input_path: pathlib.Path = pathlib.Path(conf.input).parent.resolve()
    input_file: pathlib.Path = pathlib.Path(conf.input).resolve()

    input_file = pathlib.Path(validate_metadata(str(input_file))).resolve()

    command = ["pandoc", "-s", "--toc"]
    template = conf.templates[conf.template]

    command.append(str(input_file))

    command.extend(["--reference-doc", str(reference_path / template.reference)])

    for f in conf.templates[conf.template].pandoc_filters:
        command.extend(["--filter", str(filter_path / f)])

    if not conf.highlight:
        command.extend(["--highlight-style", "monochrome"])

    command.extend(["-o", str(output_path.absolute())])
    subprocess.run(command, cwd=input_path)

    # calling handlers one by one
    for handler_name, params in conf.templates[conf.template].docx_handlers.items():
        # if a handler is set to `False` in config, then skip it
        enabled = conf.dict().get(handler_name, True)
        if not enabled:
            continue
        handler_map[handler_name](str(output_path.absolute()), **params)

    os.remove(input_file)

    return str(output_path.absolute())


if __name__ == "__main__":
    print("Please give me star if this application helps you!")
    print("如果这个应用有帮助到你，请给我点一个 star！")
    print("https://github.com/woolen-sheep/md2report")
    p = configargparse.ArgParser()
    p.add_argument(
        "-c",
        "--config",
        default="",
        required=False,
        is_config_file=True,
        help="config file path",
    )
    p.add_argument(
        "--highlight",
        default=True,
        required=False,
        help="enable highlight of code blocks",
    )
    p.add_argument(
        "-o",
        "--output",
        default="output.docx",
        required=False,
        help="output docx filename",
    )
    p.add_argument("-i", "--input", required=True, help="input markdown filename")
    p.add_argument(
        "-t", "--template", default="HUST", required=False, help="template to use"
    )
    p.add_argument(
        "--first_line_indent",
        default=True,
        required=False,
        help="enable the first line indent",
    )

    args = p.parse_args()

    if args.config != "":
        conf = load_config(vars(args), args.config)
    else:
        conf = load_config(vars(args))
    convert_md_to_docx(conf)
