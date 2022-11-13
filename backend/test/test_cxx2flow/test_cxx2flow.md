
# 流程图

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

