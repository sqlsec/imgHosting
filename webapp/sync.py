# -*- coding: UTF-8 -*-
'''
将imgHosting uploads 下的脚本信息 都录入到 webapp/db/imgHosting.db 中
'''
import os
import re

from imgHosting import uploadsPath
from View import db, IMGHOSTINGDB, UploadPoints

def getinfo(sourcePath):
    namePattern = re.compile(r'self.name\s*=\s*"(.*)"')
    authorPattern = re.compile(r'self.author\s*=\s*"(.*)"')
    maxsizePattern = re.compile(r'self.maxsize\s*=\s*(.*)')
    isUploadGifPattern = re.compile(r'self.isUploadGif\s*=\s*(True|False)')
    with open(sourcePath, 'r') as sourceFile:
        contens = ''.join(sourceFile.readlines())
        # namePattern.findall(contens)[0]
        # authorPattern.findall(contens)[0]
        # maxsizePattern.findall(contens)[0]
        # isUploadGifPattern.findall(contens)[0]
    return namePattern.findall(contens)[0], authorPattern.findall(contens)[0], maxsizePattern.findall(contens)[0], isUploadGifPattern.findall(contens)[0]

def getMaxsize(maxsize):
    if "*" in maxsize:
        a = 1
        for i in [int(num) for num in maxsize.split("*")]:
            a *= i
        return a
    else:
        return int(maxsize)


class dbsync():
    @staticmethod
    def update():
        '''
        更新数据
        '''
        pass

    @staticmethod
    def reentry():
        '''
        全部重新录入数据库
        '''
        if os.path.exists(IMGHOSTINGDB):
            os.remove(IMGHOSTINGDB)
        db.create_all()

        for upload in os.listdir(uploadsPath):
            if (not upload == "__init__.py") and upload.endswith(".py"):
                sourcePath = os.path.join(uploadsPath, upload)
                name,author,maxsize,isUploadGif = getinfo(sourcePath)
                maxsize = getMaxsize(maxsize)
                if isUploadGif == "True":
                    isUploadGif = True
                else:
                    isUploadGif = False
                db.session.add(UploadPoints(name, sourcePath, author, maxsize, isUploadGif))
        db.session.commit()


if __name__ == "__main__":
    dbsync.reentry()