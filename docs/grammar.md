# 标准语法

md2report使用的大部分是标准markdown语法，但是markdown标记到docx的样式映射可能与你的习惯不同。
按照推荐的方式使用markdown标记能生成更加规范的报告。

## 标题与副标题

大部分人在写markdown时习惯于将`H1`(`# `)作为主标题，但在md2report中，应使用`metadata`来指定标题。
H1在md2report中为一级节标题。

应该这样：

```markdown
---
title: 数据结构实验报告
subtitle: 哈夫曼编/译码器
---

# （第一节标题）
```

而不是这样：
```markdown
# 数据结构实验报告

##（第一节标题）
```

第二种写法会导致章节编号错位。

## 摘要

你可以通过添加metadata的方式为你的文档添加摘要：

```markdown
---
title: 数据结构实验报告
subtitle: 实验二-哈夫曼编/译码器
abstract_zh: 中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要中文摘要
abstract_en: English Abstract English Abstract English Abstract English Abstract English Abstract English Abstract English Abstract English Abstract English Abstract
---

# 第一节标题
```

## 章节标题

md2report支持markdown heading (H1-H9)的识别，并支持H1-H4的自动编号。因此在编写报告时请不要手动加入文本编号。

应该这样：

```markdown
# Heading text

## Heading text
```

而不是这样：

```markdown
# 1. Heading text

## 1.1 Heading text
```

## 图注

md2report会将所有的图片标题转换为图片图注，并且添加支持引用的图片编号。因此请不要留空图片标题。

```markdown
![解码](Decoding.png)
```

!!! warning

    虽然`backend/test`中的测试文件使用了中文文件名，但是在使用md2report的时候请尽量避免使用中文文件名，防止因为编码问题引起的转换失败。如果你遇到了这种情况，请放心提交issue。

## 表标题

虽然markdown并不支持表标题，但是你可以添加能被md2report识别的注解信息作为表标题：

```markdown
#table 转义序列表

| **字符** | **转义序列** | **描述**      |
| -------- | ------------ | ------------- |
| `\x0A`   | `\n`         | 换行符（LF）  |
| `\x20`   | `\b`         | 半角空格      |
| `\x09`   | `\t`         | 制表符（Tab） |
```

同样的，md2report也会为表格添加支持引用的表格编号。

# 追加特性

## cxx2flow

md2report 集成了 [cxx2flow](https://github.com/Enter-tainer/cxx2flow)，可以将c++代码转化为流程图。

````markdown

```cxx2flow:流程图标题
int main() {
    // 初始化哈夫曼树
    if (!FileExists("hfmTree.dat")) {
        tree = InitHfmTree();
    } else {
        tree->init();
    }

    // 初始化编码/解码器
    EnDecoder endecoder;
    InitEnDecoder(&endecoder, tree);

    // 输出帮助信息
    PrintHelpMsg();
    File in, out;
    while (TRUE) {
        // 读取用户指令，根据指令调用指定功能
        PrintLineHeader();
        Cmd op;
        ReadOp(&op);
        if (op == 'I') {
            tree = InitHfmTree();
        } else if (op == 'E') {
            ProcCmd(&in, &out);
            Encode(endecoder, in, out);
        } else if (op == 'D') {
            ProcCmd(&in, &out);
            Decode(endecoder, in, out);
        } else if (op == 'P') {
            ProcCmd(&in);
            PrintCode(endecoder, in);
        } else if (op == 'T') {
            ProcCmd(&out);
            PrintTree(tree, out);
        } else {
            Print("Unknow command!"); // 未知输入异常
            continue;
        }
        Print("Success!");
    }
    return 0;
}
```

````

生成效果：

![cxx2flow](img/cxx2flow.svg)

!!! note

    cxx2flow仅会生成 `main` 函数的流程图，如果有多个函数的流程图需要生成，则需要编写多个包含main函数的 `cxx2flow` 代码块。

!!! warning

    cxx2flow生成的流程图并不能完美符合部分大学对于流程图的要求，用户需自行斟酌是否使用。
