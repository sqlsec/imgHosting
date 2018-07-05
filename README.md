# imgHosting
## 使用说明
### 开发环境
依赖`pipenv`管理,具体安装参见[pipenv#installation](https://github.com/pypa/pipenv#installation)。
安装pipenv之后, 进入项目根目录（含有Pipfile文件目录），
执行以下命令，安装`imgHosting`到本地环境。
```shell
pipenv install --skip-lock
pipenv install '-e .' --dev --skip-lock
```
进入虚拟环境
```shell
pipenv shell
```
测试：
```shell
python imgHosting/uploads/GroupJD_0001.py -f imgHosting/uploads/test.png
```

### uploads编写

在`uploads`目录下:
新建文件
例如`GroupJD_0001.py`:

首先导入相关接口：
```python
from imgHosting import FreeimgUpLoad

import requests
```
定义Upload类继承FreeimgUpLoad
在`__init__`下目前就这个几个参数需要定义
`self.isUploadGif`:此上传是否支持gif图片
```python
class Upload(FreeimgUpLoad):

    def __init__(self):
        super(Upload, self).__init__()
        self.name = "京东论坛上传点"
        self.author = "hyhmnn"
        self.isUploadGif = False

    def upimag(self):
        <上传的代码>
        <返回图片的url>
```
下面看一下`GroupJD_0001.py`的`upimag`方法:
`self.filename`就是运行时`-f`指定的文件。
返回一个成功上传的图片`url`
```python
    try:
        with open(self.filename, 'rb') as file:
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
```
`run()`会解析命令行参数 -f 到 filename 中
```python
if __name__ == '__main__':
    Upload().run()
```