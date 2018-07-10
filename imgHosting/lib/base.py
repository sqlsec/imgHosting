# coding:utf-8

from imgHosting.lib.parse import create_cmd_parser
from imgHosting.lib.logout import LogOutPut

import os
from colorama import Fore


class FreeimgUpLoad(object):

    def __init__(self):
        self.logout = LogOutPut()
        self.target = None

        # 需要在Upload下完善的参数
        self.name = ""
        self.author = ""
        # 限制图片大小：已字节(k)为单位
        self.maxsize = None
        self.isUploadGif = None


    def upimag(self):
        '''
        子类 Upload 中必须覆写方法 upImag
        '''
        pass

    def run(self, filename=None):
        '''执行上传图片
        当 filename=None 时，忽略函数参数，解析命令行参数获取执行参数

        :param filename: 图片文件
        :type filename: str, None 默认为 None
        '''
        if filename is None:
            args = create_cmd_parser()
            self.target = args.filename
        else:
            self.target = filename
        
        fsize = os.path.getsize(self.target)
        if fsize > self.maxsize:
            self.logout.warning("注意图片大小！")
        else:
            result = self.upimag()
            self.logout.error(result) if "错误信息" in result else self.logout.success(result)