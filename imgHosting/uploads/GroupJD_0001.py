# coding:utf-8

from imgHosting import FreeimgUpLoad

import requests


class Upload(FreeimgUpLoad):

    def __init__(self):
        super(Upload, self).__init__()
        self.name = "京东论坛上传点"
        self.author = "hyhmnn"
        self.maxsize = 10*1024
        self.isUploadGif = False
        

    def upimag(self):
        try:
            with open(self.target, 'rb') as file:
                url = 'https://group.jd.com/ueditor/jsp/imageUp.jsp?action=uploadimage&encode=utf-8'
                headers = {
                    'Host': 'group.jd.com',
                    'Origin': 'https://group.jd.com',
                    'Referer': 'https://group.jd.com/ueditor/dialogs/imag',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',   
                }
                response = requests.post(url, headers=headers,files={'upfile':file})
                return 'http://img30.360buyimg.com/club_community/'+response.json()['url']
        except Exception as e:
            return "获取图片失败.错误信息:{0}".format(e)

if __name__ == '__main__':
    Upload().run()