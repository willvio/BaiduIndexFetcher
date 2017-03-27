# BaiduIndexFetcher
## 使用说明
1. 克隆项目到本地:  打开终端，创建并进入项目目录，输入如下命令：  
`git clone https://github.com/willvio/BaiduIndexFetcher.git`
2. 搭建虚拟环境：
 - 打开pycharm-->Configure-->Settings-->Project Interpreter-->点击小齿轮图标-->Create VirtualEnv-->输入虚拟环境的名字，路径，并指定python解释器/版本（此项目使用的版本为python3），不勾选Inherit global site-packages选项。
 - 返回pycharm欢迎界面后点击open，将目录指定到上一步克隆的项目目录，点击OK。
 - 进入pycharm，此时已进入虚拟环境，在终端中输入如下命令：  
`pip list`
可以看到此虚拟环境中已安装的包。
 - 安装本项目所需要的包：
	 - 更新pip：
	 `pip install --upgrade pip` 
	 - 安装numpy, scipy, pillow, selenium, opencv-python:
	 ` pip install numpy scipy pillow selenium opencv-python`
3. [下载ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)，放到项目目录（BaiduIndexFetcher）下。
4. 打开项目文件夹，在resource目录下找到account.txt文件，输入百度账号的用户名，换行后输入密码。
5.  运行test目录下的baiduindex.py，并按提示操作。  

### 注意：
- 程序运行中途在登录界面需要手动输入验证码
- 输入查询关键字后，程序将自动获取指数，此过程中切勿移动鼠标