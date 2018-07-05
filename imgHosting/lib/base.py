# coding:utf-8

from imgHosting.lib.parse import create_cmd_parser

from colorama import Fore


class FreeImgUpLoad():

    def __init__(self):
        self.name = ""
        self.author = ""
        self.isUploadGif = None
        self.target = None

    def upImag(self):
        '''
        子类 Upload 中必须覆写方法 upImag
        '''
        pass
    
    def outPut(self, strings):
        if "错误信息:" in strings:
            print(Fore.RED + strings)
        else:
            print(Fore.GREEN + strings)

    def run(self, filename=None):
        '''执行上传图片
        当 filename=None 时，忽略函数参数，解析命令行参数获取执行参数

        :param filename: 图片文件
        :type filename: str, None 默认为 None
        '''
        if filename is None:
            args = create_cmd_parser()
            self.filename = args.filename
        else:
            self.filename = filename
        self.outPut(self.upImag())