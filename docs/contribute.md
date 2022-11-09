# 帮助开发

## 工作原理

md2report 大体上是一个 pandoc filter ，对 pandoc 生成的 Json AST 做了一些修改，使之符合大学报告的要求。对于有些无法在 AST 中实现的修改，则使用 python-docx 修改最后生成的 docx 文件。

- pandoc filters 位于 `backend/filters` , 称其为filters。
- 调用pandoc时会使用 `--reference-doc` 参数指定模板，模板位于 `backend/reference-docs`。
- pandoc生成出docx文件后，会调用 `python-docx` 对其进行修改, 代码位于 `backend/docx_han`。

### `filters/general.py`

此文件的定位是一个通用filter，负责添加摘要、添加图注、添加表格标题等。一般来说可以直接使用这个filter。

## 环境搭建

使用poetry管理开发环境。安装poetry后：

```bash
cd backend
poetry install
poetry shell

which python
# should output a venv python

python md2report.py -h
```

## 如何添加模板

开始添加模板之前，建议先了解：

- [pandoc filter](https://pandoc.org/filters.html)
- [pandoc 文档](https://pandoc.org/MANUAL.html) 中的 `--reference-doc` 参数
- [panflute 文档](http://scorreia.com/software/panflute/)
- [python-docx 文档](https://python-docx.readthedocs.io/en/latest/)

### 新增reference doc

复制一份HUST.docx，修改为你需要的名称，然后编辑其中你需要修改的样式（比如正文样式，标题样式，页眉页脚等）。

### 新增filter

大部分情况下，可以直接使用general.py。如果你真的有需要，可以把新增的filter置于 `backend/filters` 下。

### 新增docx handler

可以参考 `hust.py`, 在这一部分可以完成你们学校的一些定制化的设定，比如学校的logo。

### 修改config

编辑 `backend/config/config.yaml`, 参考现有配置增加一个新的配置，并且指定你添加的filter和handler

!!! note

    filter和handler可以不止有一个，config中指定的是一个列表，将会被按顺序调用。

### 修改前端

如果需要，将你的配置名称添加到前端的select列表里。
