# txt2epub
py、pandoc合力打造的txt转epub自动精排自动删除多余空格空行脚本！

使用方法：
首先安装pandoc,debian系：<code>apt install pandoc</code> | arch系：<code>pacman -S pandoc</code> | 其他：自行查阅
下载本脚本将run.py和epub.css放在同一文件夹下
然后将txt小说文件和小说封面一起放入run.py所在文件夹内
用终端打开该文件夹，输入指令
```bash
python run.py
```
运行脚本
### 本脚本目前仅支持jpg/jpeg格式的图片作为封面
