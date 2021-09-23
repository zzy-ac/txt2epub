#!/usr/bin/python
print("注：请将txt和jpeg文件重命名成书名+后缀\n并将其放入脚本所在文件夹\n请查看txt的编码\n\n请务必确保文件夹内有txt和jpeg后缀的同名文件\n\n")
import os
#import re
import regex as re
import glob
import chardet
import time
import requests

cover_qidian = input('是否使用起点封面？\n（选择否将自动使用文件夹下的jpg图片为封面）[Y/N]')

os.system("mv  ~/storage/downloads/ebooks/*.txt ./")

print('正在录入书籍数据')
path = glob.glob('*.txt')
filename = str(path)[2:-6]
#bookname = bookauthor[0:bookauthor.rfind(' 作者：')]
title_string = re.search(r'(?<=《)[^》]+',filename)[0]
author_string = re.search(r'(?<=作者：).*',filename)[0]
bookname = title_string
txtname = bookname + ".txt"
jpgname = bookname + ".jpeg"
epubname = bookname + ".epub"
#title_string = bookname
#author = bookauthor[bookauthor.rfind(' 作者：'):]
#author_string = author.replace(' 作者：' , '')

if cover_qidian == 'Y':

    url = "https://m.qidian.com/search?kw=" + bookname  # 指定目标url, 注意是完整的url, 而[>
    ob = os.system('wget "%s" -O url.html --show-progress -q' % (url))	# 获取目标url对象
    f = open('url.html','r', encoding="utf-8")
    web_demo = f.read()
    f.close  # 获取目标url网页源码
    lines = web_demo.rsplit("\n") # 将源码分行列入列表
    needcode = lines[228] # 提取出图片链接所在的行
    res = re.findall(r'(//bookcover.yuewen.com/qdbimg/349573/.*150)',needcode) # 在链接所在>
    cover_url = 'https:' + res[0].replace('150','600') #将链接转换为600*800尺寸图片的链接
    os.system('wget "%s" -O "%s".jpg --show-progress -q ;rm url.html' % (cover_url,filename)) # 调用curl下载图片（别问我为什么不用python下，我菜。
elif cover_qidian == 'N':
    os.system("cp  ~/storage/downloads/ebooks/*.jpg ./ ; mv ~/storage/downloads/ebooks/*.jpg ~/storage/downloads/ebooks/cache ")
    os.system("cp  ~/storage/downloads/ebooks/*.jpeg ./ ; mv ~/storage/downloads/ebooks/*.jpeg ~/storage/downloads/ebooks/cache ; rm ~/storage/downloads/ebooks/cache")
else:
    print('Erro')
    quit()


print('书名: '+bookname+'\n'+'作者: '+author_string)

os.system('mv *.txt "%s"' % (txtname))

start = time.perf_counter()


# 开始图片处理
Your_Dir='./'
Files=os.listdir(Your_Dir)
for k in range(len(Files)):
    # 提取文件夹内所有文件的后缀
    Files[k]=os.path.splitext(Files[k])[1]

# 你想要找的文件的后缀
Str='.jpg'
if Str in Files:
    os.system("rename .jpg .jpeg *.jpg")
    print('图片转换已完成')
else:
    print('图片转换已完成') 

os.system("find ./ -name '*.jpeg' -exec convert -resize 600x800 {} {} \;")
os.system('mv *.jpeg "%s"' % (jpgname))
#图片转换结束

print("开始文件转码.......")

def detectCode(path):
    with open(path, 'rb') as file:
        data = file.read(20000)
        dicts = chardet.detect(data)
    return dicts["encoding"]

path = txtname

ecode = detectCode(path)
print('文件编码：' + ecode)
if ecode != 'utf-8' and ecode != 'UTF-8-SIG':
        f = open(txtname, 'r', encoding = "gb18030")
        content = f.read()
        f.close()
        f = open(txtname, 'w', encoding="utf-8")
        f.write(content)
        f.close()
else:
        print('文件转码完成')
print("开始格式化文本")
def replace_comma(data):
    """
    Remove the comma,\t from a string
    """ 
    return re.sub("\p{Zs}\p{Zs}+","",data)
 
def remove_old(filename_old,filename_new):
    """
    remove old file only new file exists!
    """
    aa = os.path.exists
    if aa(filename_old) and aa(filename_new):os.remove(filename_old)
    else:print("Not allowed!")
 
def deal_file(filename_old,filename_new):
    try:
        with open(filename_old,encoding="utf8") as f1:
            with open(filename_new,"a",encoding="utf8") as f2:
                for i in f1:
                    if i.strip():f2.write(replace_comma(i))
        remove_old(filename_old,filename_new)
    except BaseException as e:
        print(e)
 
 
if __name__ == '__main__':
    filename1 = txtname
    filename2 = txtname + '1'
    deal_file(filename1,filename2) 

os.renames(filename2,filename1)

print("格式化文本完成")

print('开始分章以及处理多余内容')
f = open(txtname,'r', encoding="utf-8")
content = f.read()
f.close

lines = content.rsplit("\n") 
new_content = []
new_content.append("% "+ title_string)
new_content.append("% "+ author_string)

for line in lines:
    
    if line == "更多精校小说尽在知轩藏书下载：http://www.zxcs.me/" or line == "==========================================================" or line == title_string or line == title_string + " 作者：" + author_string or line == "作者：" + author_string or line == "作者: " + author_string:
           continue
    if line == "简介:" or line == "内容简介：":
            new_content.append("### " + line + "\n")
            continue
    if re.match(r'^\s*[(楔子)(引子)(序章)].*',line):
            new_content.append("## " + line + "\n")
            continue
    if re.match(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[卷].*',line):
        new_content.append("# " + line + "\n")
        continue

    if re.match(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[章].*',line):
               new_content.append("## " + line + "\n")
               continue

    new_content.append(line + "\n")
new_content = "\n".join(new_content)

f = open(txtname,'w',encoding="utf=8")
f.write(new_content)
f.close


print("开始转换EPUB文件........")
os.system('pandoc "%s" -o "%s" -t epub3 --css=epub.css --epub-chapter-level=2 --epub-cover-image="%s"' % (txtname, epubname, jpgname))
end = time.perf_counter()
print('Running time: %s Seconds' % (end - start))
start_1 = time.perf_counter()
#os.system('kindlegen -c1 -dont_append_source "%s" > a' % (epubname))
end_1 = time.perf_counter()
#print('Running time: %s Seconds' % (end_1 - start_1))
print("删除残留文件......")
os.system('rm "%s"' % (txtname))
os.system('rm "%s"' % (jpgname))
#os.system('rm a')
os.system("mv *.epub ~/storage/downloads/ebooks")
#os.system("mv *.mobi /home/zzy/Desktop")
print("完成，收工，撒花！！🎉🎉")
