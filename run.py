print("注：请将txt和jpeg文件重命名成书名+后缀\n并将其放入脚本所在文件夹\n请查看txt的编码\n\n请务必确保文件夹内有txt和jpeg后缀的同名文件\n\n")
import os
import regex as re

filename = input("请输入书名：")
txtname = filename + ".txt"
jpgname = filename + ".jpeg"
epubname = filename + ".epub"
title_string = filename
author_string = input("请输入作者名：")
a = input("编码格式：")

os.system('mv *.txt "%s"' % (txtname))


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
f = open(txtname, 'r', encoding = a)
content = f.read()
f.close()
f = open(txtname, 'w', encoding="utf-8")
f.write(content)
f.close()

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
        print("Successfully!")
    except BaseException as e:
        print(e)
 
 
if __name__ == '__main__':
    filename1 = txtname
    filename2 = txtname + '1'
    deal_file(filename1,filename2) 

os.renames(filename2,filename1)
os.system("sleep 5s")
print("格式化文件完成")

f = open(txtname,'r', encoding="utf-8")
content = f.read()
f.close()

lines = content.rsplit("\n") 
new_content = []
new_content.append("% "+ title_string)
new_content.append("% "+ author_string)
for line in lines:
    if line == "更多精校小说尽在知轩藏书下载：http://www.zxcs.me/" or line == "==========================================================" or line == title_string or line == title_string + " 作者：" + author_string or line == "作者：" + author_string:
        continue
    
    if line == "内容简介：":
        new_content.append("# " + line + "\n")
        continue
    if re.match(r'^\s*[第卷][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[章卷].*',line):
        new_content.append("# " + line + "\n")
        continue
    new_content.append(line + "\n")
new_content = "\n".join(new_content)

f = open(txtname,'w',encoding="utf=8")
f.write(new_content)
f.close


print("开始转换EPUB文件........")
os.system('pandoc "%s" -o "%s" -t epub3 --css=epub.css --epub-cover-image="%s"' % (txtname, epubname, jpgname))
print("删除残留文件......")
os.system('rm "%s"' % (txtname))
os.system('rm "%s"' % (jpgname))
os.system("mv *.epub /home/zzy/Desktop")
print("完成，收工，撒花！！🎉🎉")
