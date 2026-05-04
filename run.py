#!/usr/bin/python
#print("注：请将txt和jpeg文件重命名成书名+后缀\n并将其放入脚本所在文件夹\n请查看txt的编码\n\n请务必确保文件夹内有txt和jpeg后缀的同名文件\n\n")
import os
#import re
import regex as re
import glob
import chardet
import time
import requests
import sys
from PIL import Image
cover_qidian = input('是否使用起点封面？[Y/N]')
 
print('正在录入书籍数据')
os.system('mv ~/storage/downloads/ebooks/*.txt ./')

path = glob.glob('*.txt')
filename = str(path)[2:-6]
#bookname = bookauthor[0:bookauthor.rfind(' 作者：')]
title_string = re.search(r'(?<=《)[^》]+',filename)[0]
author_string = re.search(r'(?<=作者：).*',filename)[0]
bookname = title_string
txtname = bookname + ".txt"
jpgname = bookname + ".jpeg"
epubname = bookname + ".epub"
kepubname = bookname + ".kepub.epub"
#title_string = bookname
#author = bookauthor[bookauthor.rfind(' 作者：'):]
#author_string = author.replace(' 作者：' , '')

if cover_qidian == 'Y' or cover_qidian == 'y' or cover_qidian == '':
    
    print('开始下载封面')
# 下载起点url网页，以便查找封面图片链接

    url = 'https://m.qidian.com/soushu/' + bookname + '.html'  # 指定目标url
    
    # 添加User-Agent和其他常见浏览器头，以模拟浏览器请求，避免WAF拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    response = requests.get(url, headers=headers, stream=True) # 在这里传入headers
    response.raise_for_status() # 检查请求是否成功

    with open('url.html', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
      	    if chunk:
                f.write(chunk)

    ob = response
    urlname = 'url.html'
    with open("url.html", "r", encoding="utf-8") as f:
        html_content = f.read()

# 使用正则表达式提取第一个匹配的 data-src 属性值
    match = re.search(r'data-src="([^"]+)"', html_content)
    if match:
        res = match.group(1)[:-3]
        print("data-src value:", res)
    else:
        print("No data-src value found. HTML content might be a WAF page or unexpected format.") # 增加提示
        # 可以选择在这里打印html_content以便调试
        # print(html_content)


# 下载封面图片
    cover_url = 'https:' + res + '600' #将链接转换为600*800尺寸图片的链接
    response = requests.get(cover_url, stream=True)
    with open(f'{filename}.jpg', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    os.remove('url.html')


# 选择本地图片
elif cover_qidian == 'N' or cover_qidian == 'n':
	jpgfile=input('请输入封面图片路径：').replace("\n","").replace("'","").replace(" ","")
	os.system('cp "%s" ./' % jpgfile)
else:
    print('Erro')
    quit()


print('书名: '+bookname+'\n'+'作者: '+author_string)

os.system('mv *.txt "%s"' % (txtname))

start = time.perf_counter()


# 开始图片处理

def IsValidImage(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid

def transimg(path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    for image in os.listdir(path):
        img_path = path + '/' + image
        if IsValidImage(img_path):
            try:
                str = img_path.rsplit(".")
                if str[-1] == 'jpg' or str[-1] == 'jpeg' or str[-1] == 'JPG' or str[-1] == 'JPEG':
                    pass
                else:
                    str = img_path.rsplit(".", 1)
                    output_img_path = str[0] + ".jpeg"
                    im = Image.open(img_path)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(output_img_path)
                    os.remove(img_path)
            except:
                pass
        else:
            pass

if __name__ == '__main__':
    path = './'
    transimg(path)

[Image.open(os.path.join(dp, f)).resize((600, 800), Image.Resampling.LANCZOS).save(os.path.join(dp, f), format='JPEG', quality=85) for dp, _, fn in os.walk('.') for f in fn if f.lower().endswith(('.jpeg', '.jpg'))]
os.system('rename *.jpeg "%s" *.jpeg' % jpgname)
#图片转换结束

print("开始文件转码.......")

def detectCode(path):
    with open(path, 'rb') as file:
        data = file.read(20000)
        dicts = chardet.detect(data)
    return dicts["encoding"]

path = txtname

ecode = detectCode(path)

#print('文件编码：' + ecode)
#如果ecode中包含“gb”则说明是gbk编码，将ecode改为gbk

if ecode != 'utf-8' and ecode != 'UTF-8-SIG':
    if 'GB' or 'gb' in ecode:
        ecode = 'gbk'
    else:
        pass 
    print("文件编码不是utf-8,开始转换.....")
    f = open(txtname, 'r', encoding = ecode, errors="ignore")
    content = f.read()
    f.close()
    f = open(txtname, 'w', encoding="utf-8", errors="ignore")
    f.write(content)
    f.close()
    print("转换完成")
else:
    print('文件编码是utf-8，无需转换')
        
print("开始格式化文本")
def replace_comma(data):
    """
    Remove the comma,\t from a string
    """ 
    return re.sub(r"\p{Zs}\p{Zs}+","",data)
 
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

#print("格式化文本完成")

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
    if line == "简介:" or line == "内容简介：" or line == "内容简介":
            new_content.append("### " + line + "\n")
            continue
    if re.match(r'^\s*(楔子|序章|序言|序|引子).*',line):
            new_content.append("## " + line + "\n")
            continue
    if re.match(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[卷].*',line):
        new_content.append("# " + line + "\n")
    if re.match(r'^\s*[卷][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[ ].*',line):
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


print("开始生成EPUB文件........")
os.system('pandoc "%s" -o "%s" -t epub3 --css=epub.css --split-level=2 --epub-cover-image="%s"' % (txtname, epubname, jpgname))
end = time.perf_counter()
print('Running time: %s Seconds' % (end - start))
start_1 = time.perf_counter()
#os.system('kindlegen -c1 -dont_append_source "%s" > a' % (epubname))
os.system('./kepubify -i "%s"' % (epubname))
end_1 = time.perf_counter()
#print('Running time: %s Seconds' % (end_1 - start_1))
print("删除残留文件......")
os.system('rm "%s"' % (txtname))
os.system('rm "%s"' % (jpgname))
#os.system('rm a')
#os.system('mv *.kepub.epub "%s"' % (kepubname))
os.system('mv "%s" ~/storage/downloads/ebooks' % (epubname))
os.system('mv "%s" ~/storage/downloads/ebooks' % (kepubname))
#os.system("mv *.mobi /home/zzy/Desktop")
print("完成，收工，撒花！！🎉🎉")
