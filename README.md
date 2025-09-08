# **环境依赖**
1. 安装 adb 环境
2. python 环境执行 pip install -r requirements.txt 安装依赖包


# **目录结构描述**
##### ├──cocos                                _# 打包到客户端代码中_
##### │   ├── *                               _# 省略_
##### ├──common                               _# 通用文件夹_
##### │   ├──base_page.py                     _# 页面基类的封装基础操作_
##### │   ├──rpc_method_request.py            _# 与c#的rpc通信_
##### │   ├──error.py                         _# 自定义的错误类型_
##### ├──configs                              _# 配置文件夹_
##### │   ├──elements_data.py                 _# 元素定位信息_
##### ├──panelObjs                            _# 各页面的具体方法_
##### │   ├── *                               _# 省略_
##### ├──scripts                              _# 由各页面的具体方法组成的测试用例_
##### │   ├── *                               _# 省略_
##### ├──tools                                _# 工具文件夹_
##### │   ├── common_tools.py                 _# 通用工具方法_
##### ├──requirements.txt                     _# 项目依赖包_


# **PC-浏览器运行-配置**
1. cmd命令窗口执行命令打开谷歌浏览器，开启远程端口访问
```
open -a "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_profile
或
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_profile"
或
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_profile"
```
2. Cocos Creator 选择浏览器预览模式运行客户端
3. 浏览器窗口保持默认分辨率
4. 编写脚本：浏览器缩放100%，通过"R键"打开/关闭元素获取模式
5. 执行时：通过浏览器缩放保证整个游戏界面展示完整


# **安卓设备运行-配置**
1. 打开cmd命令窗口输入 adb devices 命令，获取设备号
```    
adb devices
```
2. 打开common/base_page.py，将 serial_number 替换为步骤一获取到的设备号
```    
    def __init__(self):
        self.serial_number = "设备号"
```


# **苹果设备运行-配置**
1. usb连接电脑，xcode在手机上安装WebDriverAgent并启动
```    
https://github.com/appium/WebDriverAgent
https://cm9cs07irw.feishu.cn/docx/BxPKdcDrzo6a0axGsQMcRokLnoh
```


### **#运行用例**
1.可以运行scripts文件夹下的测试用例
    使用方式为：打开guide_test.py文件，右键运行







