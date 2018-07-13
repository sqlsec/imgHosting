# -*- coding: UTF-8 -*-

import os
import re
import hashlib
# from werkzeug import secure_filename
from flask import Flask, render_template, request, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


app = Flask(__name__)
# settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "fileupload/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# sqlite db setting
IMGHOSTINGDB = os.path.join(BASE_DIR, "db/imgHosting.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(IMGHOSTINGDB)
db = SQLAlchemy(app)


# UploadPoints models
class UploadPoints(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 上传点的name 是唯一的
    name = db.Column(db.String(200), unique=True, nullable=True)
    sourcepath = db.Column(db.String(300), unique=True, nullable=True)
    author = db.Column(db.String(200), nullable=True)
    maxsize = db.Column(db.Integer, nullable=True)
    isUploadGif = db.Column(db.Boolean, nullable=True)

    def __init__(self, name, sourcepath, author, maxsize, isUploadGif):
        self.name = name
        self.sourcepath = sourcepath
        self.author = author
        self.maxsize = maxsize
        self.isUploadGif = isUploadGif

    def __repr__(self):
        return self.name


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_filename_md5(filename, sendType="md5"):
    if filename !=None and sendType=="md5":
        filetype = filename.rsplit('.', 1)[1]
        return get_str_md5(filename.rsplit('.', 1)[0])+"."+filetype

def get_str_md5(string, sendType="md5"):
    if string !=None and sendType=="md5":
        m = hashlib.md5()
        m.update(string.encode("utf-8"))
        return m.hexdigest()


# 读取数据
def get_dbdata():
    pass

# 判断文件是否超出上传点的限制大小
def overflowMaxsize(point, filepath):
    filesize = os.path.getsize(filepath)
    if filesize > point.maxsize:
        return True
    else:
        return False

# 删除文件
def delete_img(imgpath):
    if os.path.exists(imgpath):
        os.remove(imgpath)

# 运行imgHosting下的提交脚本
def upimagRun(point,imgPath):
    shell = "python {} -f {}".format(point.sourcepath, imgPath)
    resultinfo = os.popen(shell).read()
    if "Succ" in resultinfo:
        return {"result":"success", "content":re.findall(r"(http(s|)://.*)", resultinfo)[0][0]}

    elif "Error" in resultinfo or "Warning" in resultinfo:
        return {"result":"error", "content":resultinfo.split('\n')[1]}

def isgifADNcanUploads(point, filename):
    if filename.rsplit('.', 1)[1] == "gif":
        if point.isUploadGif:
            return True
        else:
            return False
    else:
        return True

@app.route('/', methods=['GET'])
def index():
    result = "上传图片前来逛逛我的博客(*╹▽╹*)~ http://www.imipy.com"
    upload_list=UploadPoints.query.all()
    return render_template("index.html", title='index', result=result, upload_list=upload_list)

@app.route('/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file =  request.files['imgFile']
        except:
            return jsonify({"result":"error", "content":"请选择图片！"})
        pointName = request.form['choicePoint']
        try:
            isDeleteImg = True if request.form['imgdelete'] else False
        except:
            isDeleteImg = False
        point = UploadPoints.query.filter_by(name=pointName).first()
        if file and allowed_file(file.filename):
            # 如果文件是gif的，判断point是否可以上传
            if isgifADNcanUploads(point, file.filename):
                # filename = secure_filename(file.filename)
                filename_md5 = get_filename_md5(file.filename)
                file_full_path =os.path.join(app.config['UPLOAD_FOLDER'], filename_md5)
                file.save(file_full_path)
                # 判断文件是否超出上传点的限制大小
                if overflowMaxsize(point, file_full_path):
                    return jsonify({"result":"error", "content":"图片大小已经超出的({0}限制{1})".format(pointName, point.maxsize)})
                # 使用imghosting/uploads所选的脚本 提交
                result = upimagRun(point, file_full_path)
                # 上传完是否删除缓存图片
                if isDeleteImg:
                    delete_img(file_full_path)

                return jsonify(result)
            else:
                return jsonify({"result":"error","content":"该上传点不支持gif"})
        else:
            return jsonify({"result":"error", "content":"请上传图片文件(例如如下格式'png', 'jpg', 'jpeg', 'gif')"})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')