# txt2epub
py、pandoc合力打造的txt转epub自动精排自动删除多余空格空行脚本！

### 2021 6.21  更新内容：
1、自动设置文件名为书名<br/>
2、自动识别编码格式，不在需要手动设置<br/>
3、支持生成mobi格式（调用kindlegen）<br/>

使用方法：<br/>
首先安装pandoc,debian系：<code>apt install pandoc</code> | arch系：<code>pacman -S pandoc</code> | 其他：自行查阅<br/>
下载本脚本将run.py和epub.css放在同一文件夹下<br/>
然后将txt小说文件和小说封面一起放入run.py所在文件夹内<br/>
用终端打开该文件夹，输入指令<br/>
```bash
python run.py
```
运行脚本
### 本脚本目前仅支持jpg/jpeg格式的图片作为封面
