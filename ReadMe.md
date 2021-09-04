# HITSZ自动登录脚本
还在为没有图形界面的服务器需要登录网络准入认证系统而发愁吗？快来试试这个小脚本吧！
## Requirements
在你需要登陆的机器上至少要有...
 - ssh
 - python3.7
## 使用流程

脚本会用到`selenium`库，但是你多半没有网络没法`pip install selenium`。没关系，找一台能连上网的电脑，用它下载好依赖：
```bash
pip download selenium
```
这会把selenium和它的依赖下到本地来。然后你需要将这些.whl文件拷到目标机器里（用scp之类的）然后用pip把这些文件安装上。  

脚本会用到phantomjs。phantomjs是一个headless browser，可以在[这里](https://phantomjs.org/download.html)下载到。接下来，你既可以将它放进PATH里，也可以在执行脚本时指定它所在的目标地址（见下）。  

一切准备就绪，你可以执行
```bash
python3 main.py --username 你的用户名 --password 你的密码
```
以执行登录流程。如果希望执行phantomjs的路径，在后面添加`--phantomjs_path /path/to/phantomjs`；如果希望手动指定登录方的ip地址，在后面添加`--user_ip 你的ip`。
执行完成后，它会在当前目录下生成一张`result.png`的截图，可以用来检查登录是否成功。没生成这张图就肯定是没成功。