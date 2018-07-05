# coding: utf-8

from imgHosting import FreeimgUpLoad

import requests
import json


class Upload(FreeimgUpLoad):

    def __init__(self):
        super(Upload, self).__init__()
        self.name = "FreeBuf上传点"
        self.author = "国光"
        self.isUploadGif = True

    def upimag(self):
        try:
            with open(self.filename, 'rb') as file:
                url = 'http://www.freebuf.com/buf/plugins/ueditor/ueditor/php/imageUp.php?&post_id='
                headers = {
                    'Cookie':'3cb185a485c81b23211eb80b75a406fd=1529045953; Hm_lvt_cc53db168808048541c6735ce30421f5=1529045957,1529246161; acw_tc=AQAAABCx0Xx00gMANBLOt2cOXOmatLy0; acw_sc__=5b2a6741e23733ca2c4f902c823361a8ea25ca86; PHPSESSID=85p73eamjnti741gmd42hof9n2',
                    'Host': 'www.freebuf.com',
                    'Origin': 'http://www.freebuf.com',
                    'Referer': 'http://www.freebuf.com/video/175166.html',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
                }
                response = requests.post(url,headers=headers,files={'upfile':file}).text
                return "http://image.3001.net/" + json.loads(response.replace("'",'"'))['url'].replace("!small","")
        except Exception as e:
            return "获取图片失败.错误信息:{0}".format(e)

if __name__ == '__main__':
    Upload().run()