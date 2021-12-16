# txt2epub
py、pandoc合力打造的txt转epub自动精排自动删除多余空格空行脚本！

### 2021 12.16 更新内容：

1、支持kepub格式转换(可选)（依赖于kepubify）

2、将run1.py合并到run.py,移除run2.py,需要用到菠萝包自动获取封面的功能请自行前往[https://github.com/Elaina-Alex/txt2epub](https://github.com/Elaina-Alex/txt2epub)分支进行使用

### 2021 9.22  更新内容：

1、支持自动从起点下载封面（可选）
### 2021 9.20  更新内容：
1、新增<code>run1.py</code>以支持二级目录其中第一级为卷第二集为章，有需要可自行修改
2、新增对“引子”“序言”“序章”“序”“楔子”等的章节索引。
### 2021 7.16  更新内容：
1、新增每种格式转换耗时显示
2、新增kindlegen静默输出
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
### 书籍元数据的书名是txt的文件名
