"""
- 爬取内容：文字笑话
- 来源：糗事百科
- 显示方式：屏幕贴图
- 关闭显示：双击可关闭贴图（结合snipaste）
- 时间间隔：默认半小时一次，可设置
"""

import os
import requests
import time
import random
import win32api #用于模拟键盘F3按下，用于snipaste，可删
import win32con #同上
from lxml import etree

class Spider():
    #初始化
    def __init__(self):
        # self.headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
        # }
        #filePath是自定义的，本次程序运行后创建的文件夹路径，存放各种需要下载的对象。
        self.filePath = ('/糗事百科/'+ '文字' + '/')
        self.filePath_txt = (self.filePath + 'qiushi' + '.txt' )

    def init_filePath(self):
        #新建本地的文件夹路径，用于存储网页、图片、文字等数据！
        filePath = self.filePath
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        
        filePath_txt = self.filePath_txt
        if os.path.exists(filePath_txt):
            os.remove(filePath_txt)

    def getIds(self):
        #此函数可以获取给定页面中所有段子的id，用List形式返回
        url = "https://www.qiushibaike.com/text/"
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            qiushi_id_list = selector.xpath('//div[@class="article block untagged mb15 typs_hot"]/@id')
        except Exception as e:
            print("getIds")
            print(repr(e))
        return qiushi_id_list

    def download_text(self, qiushi_tag_id):
        #下载
        id = qiushi_tag_id.strip('qiushi_tag_')
        url = ('https://www.qiushibaike.com/article/{}').format(id)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            qiushi_text_list = selector.xpath('//div[@class="content"]/text()')
            qiushi_real_text = ""
            for text in qiushi_text_list:
                qiushi_real_text += text + '\n'
            qiushi_real_text = str(qiushi_real_text).lstrip('\n\n')
            # print(qiushi_text_list)
        except Exception as e:
            print("download")
            print(repr(e))

        self.save_file(qiushi_real_text)

    def save_file(self, qiushi_real_text):
        #存储到本地txt文件
        filePath_txt = self.filePath_txt
        try:
            f = open(filePath_txt,'a')
            f.write(qiushi_real_text)
            f.close()
            # print("qiushiText:{} has been downloaded!".format(qiushi_tag_id))
            # time.sleep(random.uniform(0,1))
        except Exception as e:
            print("save file")
            print(repr(e))

    def main_fuction(self):
        #获取糗百文字段子
        self.init_filePath()
        qiushi_tag_ids = self.getIds()
        count = 0
        for qiushi_tag_id in qiushi_tag_ids:
            self.download_text(qiushi_tag_id)
            count += 1
            #只存3个
            if count == 3:
                break

        if not os.path.exists('E:\snipaste\Snipaste.exe'):#启动记事本
            os.system(('start notepad {}').format(self.filePath_txt))
        else:#启动 Snipaste.exe 的F3贴图功能
            os.system('start ' + 'E:\snipaste\Snipaste.exe')
            time.sleep(2)
            os.system(('clip < {}').format(self.filePath_txt))
            win32api.keybd_event(0x72,0,0,0)     
            win32api.keybd_event(0x72,0,win32con.KEYEVENTF_KEYUP,0) 

spider = Spider()
spider.main_fuction()