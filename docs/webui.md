# webui

在使用[webui](https://md2report.hust.online)时，如果要上传zip文件：

- md文件应位于zip文件的根目录，而不应该在子文件夹中，参考`backend/test/test_case.zip`
- 尽量使用英文命名，并且不包含空格

!!! warning

    WebUI仅为不会使用python的用户提供便利，不能保证可用性，也不保证是最新版本。大体积文件建议使用CLI。请不要上传zip bomb，如果服务受到攻击可能考虑关闭服务。
