"""
-------------------------------------------------
File Name：run

Change Activity:

2021/9/30: V1.0: 重构代码，添加菠萝包API接口获取书籍和封面数据
2021/10/2: V1.1: 优化代码，删去无用判断
-------------------------------------------------
"""

import requests
import time
import chardet
import glob
import re
from PIL import Image
from io import BytesIO
import os



class Epub:
    def __init__(self):
        self.novelName = ''
        self.NovelTXTName = ''
        self.NovelPictureName = ''
        self.NovelEpubName = ''


    def get_request(self, url):
        headers = {"Host":"api.sfacg.com","Connection":"keep-alive","Accept":"application\/vnd.sfacg.api+json;version=1","User-Agent":"boluobao\/4.5.52(iOS;14.0)\/appStore","Accept-Language":"zh-Hans-US;q=1","Authorization":"Basic YXBpdXNlcjozcyMxLXl0NmUqQWN2QHFlcg=="}
        return requests.get(url, headers=headers).json()
        
    def GetJPG(self, url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"}
        return requests.get(url, headers=headers)
        
    def WriteTXT(self, path, x, info):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(info)
    
    
    def GetName(self):
        print('正在录入书籍数据')
        getcwd_path = glob.glob('*.txt')
        filename = ''.join(getcwd_path).split('.')[0]
        print(filename)
        searchbook = f"https://api.sfacg.com/search/novels/result?q={filename}&expand=novels%2CsysTags&sort=hot&page=0&size=12"
        novelId = [novels['novelId'] for novels in self.get_request(searchbook)['data']['novels']]
        self.novelid = ''.join(map(str, novelId))
    def get_book(self):
        self.GetName()
        url = f'https://api.sfacg.com/novels/{self.novelid}?expand=intro%2CbigNovelCover%2Ctags%2CsysTags'
        data = self.get_request(url)['data']
        # print(data)
        """书名，作者名，签约，收藏，字数"""
        self.novelName, self.authorName, self.signStatus, self.markCount, self.novelCover, self.charCount = (
            data['novelName'], data['authorName'], data['signStatus'], data['markCount'], 
                data['novelCover'], data['charCount'])
                
        """最后更新日期， 书籍状态[完结或未完]"""
        self.lastUpdateTime, self.allowDown = re.sub(r'T', " ", data['lastUpdateTime']), '未完' if data['allowDown'] else '未完'
        """简介信息，s级大图，标签，web链接，APP链接"""
        self.bigNovelCover, self.sysTag, web_url, APP_url = (
            data['expand']['bigNovelCover'], ','.join([tag['tagName'] for tag in data['expand']['sysTags']]),
                f"https://book.sfacg.com/Novel/{self.novelid}/", f"https://m.sfacg.com/b/{self.novelid}/")
                    
        Details = "小说书名:{}\n小说作者:{}\n签约状态:{}\n收藏数量:{}\n小说字数:{}\n书籍序号:{}\n".format(
        self.novelName, self.authorName, self.signStatus, self.markCount, self.charCount, self.charCount, self.novelid)
        Details += "小说标签:{}\n最后更新:{}\n小说状态:{}\n网页链接:{}\n手机链接:{}\n".format(
            self.sysTag, self.lastUpdateTime, self.allowDown, web_url, APP_url)
        Details += "小说简介:"
        intro = [re.sub(r'^\s*', "\n　　", line) for line in data['expand']['intro'].split("\n") if re.search(r'\S', line) != None]
        Details += ''.join(intro)
        self.Details = Details
        
        
    
    def epubs(self):
        self.get_book()
        save_jpg_path = os.path.join('jpg', self.novelName)
        """使用requests库下载图片"""
        if not os.path.exists(save_jpg_path):
            os.makedirs(save_jpg_path)
            print(f'已在{save_jpg_path}创建文件夹')
        with open(os.path.join(save_jpg_path, f'{self.novelName}.jpg'), 'wb') as save:
            save.write(self.GetJPG(self.novelCover).content)

        # 开始图片处理
        FileName_list = os.listdir(save_jpg_path)
        # 转换格式
        for extensions in FileName_list:
            if '.jpg' in extensions:
                extensions_jpeg = re.sub(r'.jpg', ".jpeg", extensions)
                os.rename(os.path.join(save_jpg_path, extensions), os.path.join(save_jpg_path, extensions_jpeg))

                print(f"已将 {extensions} 转为 {extensions_jpeg} ")
            else:
                print("文件夹里没有JPG图片")
        self.NovelTXTName, self.NovelPictureName, self.NovelEpubName = (
            f'{self.novelName}.txt', os.path.join(save_jpg_path, f'{self.novelName}.jpeg'), f'{self.novelName}.epub')
        
    
    def detectCode(path):
        with open(path, 'rb') as file:
            data = file.read(20000)
            dicts = chardet.detect(data)
        return dicts["encoding"]
    
    
    def codes(self):
        code_info = self.detectCode(self.NovelTXTName)
        print('文件编码:', code_info)
        if code_info != 'utf-8' and code_info != 'UTF-8-SIG':
            print("开始格式化文本")
            with open(self.NovelTXTName, 'r', encoding="gb18030") as f:
                content = f.read()
            self.WriteTXT(self.NovelTXTName, 'w', content)
        else:
            print('文件转码完成')
    
    
    
    def re_novel(self):
        read_txt = open(self.NovelTXTName, encoding="utf8") 
        content = [re.sub(r'^\s*', "　　", line) for line in read_txt.readlines() if re.search(r'\S', line) != None]
        self.WriteTXT(self.NovelTXTName, 'w', ''.join(content))
    
    def new_epub(self):
        new_content = []
        new_content.append("% "+ self.novelName)
        new_content.append("% "+ self.authorName)
        self.re_novel()
        print("格式化文本完成,开始分章以及处理多余内容")
        with open(self.NovelTXTName, 'r', encoding="utf-8") as f:
            content = f.read()
        new_content.append(self.Details)
    
        for line in content.rsplit("\n"):
            if line == self.novelName or line == f"作者：{self.authorName}":
                continue
            if line == "作者：" + self.authorName:
                continue
            if line == "名称：" + self.novelName:
                continue
            if line == "序号：" + self.novelid:
                continue
            if line == "标签：" + self.sysTag:
                continue
            if line == "简介:" or line == "内容简介：":
                new_content.append("### " + line + "\n")
                continue
            if re.match(r'^\s*[(楔子)(引子)(序章)].*', line):
                new_content.append("## " + line + "\n")
                continue
            if re.match(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[卷].*', line):
                new_content.append("# " + line + "\n")
                continue
            if re.match(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两]*[章].*', line):
                new_content.append("## " + line + "\n")
                continue

            new_content.append(line + "\n")
        new_content = "\n".join(new_content)
        
        
        self.WriteTXT(self.NovelTXTName, 'w', "".join(new_content))
        print("开始转换EPUB文件........")
        os.system('pandoc "%s" -o "%s" -t epub3 --css=epub.css --epub-chapter-level=2 --epub-cover-image="%s"' %
                  (self.NovelTXTName, self.NovelEpubName, self.NovelPictureName))
        print("完成，收工，撒花！！🎉🎉")

if __name__ == '__main__':
    Epub = Epub()
    Epub.epubs()
    Epub.new_epub()
    