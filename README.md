# DoubanRobot

Simple distributed crawler for Douban User Information.

## 依赖库：

- BeautifulSoup4: `$ pip install BeautifulSoup4`

- lxml: `$ pip install lxml`

- requests: `$ pip install requests`

- pillow: `$ pip install pillow`

## 使用：

### 需设置的内容：

1.登录时`login.py`需要豆瓣账号：`form_email`, `form_password`

    self.payload = {
        'form_email': 'example@email.com',
        'form_password': 'password',
        'remember': 'on'
    }
    
2.`manager.py`中需设置初始任务ID，与`worker`通信的端口，爬虫延迟时间。

    INIT_ID = '130949863'
    PORT = 5000
    DELAY_TIME = 5
    
3.`worker.py`中需设置运行`manager`的主机地址，通信端口，爬虫延迟时间。

    SERVER_ADDR = '127.0.0.1'
    PORT = 5000
    DELAY_TIME = 5
    
### 运行：

一台主机作为控制节点运行`manager.py`，另外若干台主机作为爬虫节点运行`worker.py`，也可以在同一台机器上同时运行一个`manager`进程和若干个`worker`进程。用户信息、已完成ID、待完成ID、headers和cookies分别保存在当前目录下的`info.txt`, `done.txt`, `todo.txt`, `session.txt`文件中。

**注意** 控制好爬虫延迟时间，速度过快会返回`403 Forbidden`、`302 Temporarily Moved`错误信息甚至封禁IP。