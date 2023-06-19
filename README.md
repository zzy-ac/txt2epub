# txt2epub

py、pandoc合力打造的txt转格式自动精排脚本！

支持输出格式：epub(通用)、kepub(kobo)、azw3(kindle|安卓端不支持)

# linux设备教程

```bash
#安装
git clone https://github.com/zzy-ac/txt2epub.git
cd txt2epub
wget https://raw.githubusercontent.com/zzy-ac/txt2epub/termux/requirements.txt
pip3 install -r requirements.txt
rm -rf requirements.txt
#运行
python3 run.py </path/of/novel>
```

# Android设备教程

## 安装txt2epub

1、安装termux

2、切换清华镜像源：

```bash
sed -i 's@^\(deb.*stable main\)$@#\1\ndeb https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main stable main@' $PREFIX/etc/apt/sources.list
apt update&&apt upgrade
```

3、运行如下指令：

```bash
curl https://gh.dmnb.cf/https://github.com/zzy-ac/txt2epub/releases/download/files/install.sh | bash
```

## 使用txt2epub

1. 将txt小说重命名为`《书名》作者：作者名.txt`的形式，并放入手机Download目录下的ebooks文件夹(如果没有这个文件夹请自建一个)

2. 在termux中运行`txt2epub`指令进行转格式，转格式生成的epub和kepub文件会放到手机的Download/ebooks目录中

# windows设备提示

~~本人没有windows设备，各位自行琢磨，原理跟linux差不多。~~

~~自己把pandoc和kepubify的exe版本下载到txt2epub文件夹然后把run.py中相关的路径修改一下 应该就好了。~~

~~之前看得太疏忽了，这个脚本还用到了一大堆什么cp、mv、cat、wget等等的linux/unix指令，Windows要用还要改不少东西，有感兴趣的可以去改一改，我不用win的就懒得弄了（都用windows了直接easypub不香吗？搁这折腾个屁，这脚本就是因为linux下面没有easypub，calibre又太慢了所以才写的）~~
在chatgpt和天翼云电脑的帮助下，于2023年4月5日，实现了脚本中引用的shell指令向python原生脚本的转换，完成了对windows平台的支持，在天翼云电脑的win server2016环境中运行正常，win版本采用直接打包压缩包的形式，压缩包内放置了kepubify、kindlegen、pandoc等程序的二进制程序，方便windows用户无脑使用。
经过测试目前可将命名格式符合要求的文本直接拖动到run.py文件上来一键生成epub和kepub文件（需将py文件的默认打开方式设置为Python,如下图：
![https://cdn.dmnb.cf/gh/zzy-ac/My-Selves-Cloud@main/images/2023/6/19/图片_c6ba92cfc5c6e17808aad708dc3163c1.png](https://cdn.dmnb.cf/gh/zzy-ac/My-Selves-Cloud@main/images/2023/6/19/图片_c6ba92cfc5c6e17808aad708dc3163c1.png)

#### windows版本注意事项：千万要看`压缩包里的必读！！不然出错不负责.md`文件

---

---我是分割线---

---



### 2022 04.08 更新内容：

1、支持包括jpg、png、webp等在内的大部分主流图片作为封面

2、为了图自己使用方便已经设置成自动从zxcs.me提供的txt文件名中获取书名和作者名，使用者可自行更改为其他规则

3、支持将文件路径传参直接使用，例如

```python
python3 run.py /path/to/AAA.txt
```

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



### ~~本脚本目前仅支持jpg/jpeg格式的图片作为封面~~

## 已支持全格式封面图片

### 书籍元数据的书名是txt的文件名
