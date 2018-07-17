# imgHosting

## 开发使用说明

### 开发环境


依赖`pipenv`管理,具体安装参见[pipenv#installation](https://github.com/pypa/pipenv#installation)。


安装pipenv之后, 进入项目根目录（含有Pipfile文件目录），

 

执行以下命令，安装`imgHosting`到本地环境。

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

 

在`uploads`目录下，新建文件：

 

例如`GroupJD_0001.py`:

 

首先导入相关接口：

```python

from imgHosting import FreeimgUpLoad

 

import requests

```

定义Upload类继承FreeimgUpLoad

 

```python

class Upload(FreeimgUpLoad):

 

    def __init__(self):

        super(Upload, self).__init__()

        # <上传点的名称> **(唯一的)

        self.name = "京东论坛上传点"

        # <作者>

        self.author = "author"

        # <是否支持gif上传> (True|False)

        self.isUploadGif = True|False

 

        # <图片上传限制 单位字节> (数字|或者数字相乘)

        self.maxsize = 10*1024*1024

 

    def upimag(self):

        # <上传的代码>

        # <方法只返回图片的url>

```

下面看一下`GroupJD_0001.py`的`upimag`方法:

 

> `self.target`会获取运行时`-f`指定的图片。

 

```python

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

```

`run()`会解析命令行参数 -f 到 target 中等，详细看(`imgHosting/imgHosting/lib/base.py` 的`run`方法)

```python

if __name__ == '__main__':

    Upload().run()

```

 

---

## webApp使用说明

> 考虑到命令行不太友好，故想搞个web端(之后想封装到docker下)

 

### 功能演示：

> 推荐用`chrome`打开...

![](http://image.3001.net/images/20180713/15314706717377.gif)

 

### 简单说一下细节

> 页面写很烂...前段知识匮乏…导致拖了些时间... o(╥﹏╥)o

 

- 前段:`bootstrap`

- web框架:`flask`

- 数据库:`sqllite`

 

### 如何使用

 

- 进入虚拟环境 

看上面进入`开发使用说明/开发环境`👆👆👆


- 同步数据

> 将imghosting/uploads 下的上传脚本录入数据库

```shell
cd webapp
python sync.py # 目前只写重新录入功能，更新没有写
```
- 运行

```shel
python View.py
```

在浏览器(推荐chrome)打开 http://localhost:5000/
