# coding = utf-8
import os, sys

# 得到该文件的上一个路径（相当于cd..）
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# 日志存放D盘，没有则放C盘
if os.path.exists('d:'):
    LOG_BASE_DIR = 'D:/'
else:
    LOG_BASE_DIR = 'C:/'

# 1.当导入一个模块时：import xxx，默认情况下python解析器会搜索
#  当前目录、已安装的内置模块和第三方模块，搜索路径存放在sys模块的path中
# 2.sys.path返回一个列表
# 3.运行时修改，脚本运行后就会失效
sys.path.append(BASE_DIR)

# 配置文件
CONFIG_DIR = os.path.join(BASE_DIR, "myConfig", "baseConfig.ini")
# 设备信息
DESIRED_CAPS = os.path.join(BASE_DIR, "myConfig", "desired_caps")
# 测试用例目录
TESTCASE_DIR = os.path.join(BASE_DIR, "Case")
# 错误截图目录
TEST_ERROR_Image = os.path.join(LOG_BASE_DIR, "logs", "image").replace('\\', '/')
# 基础图片库
TEST_BASE_IMAGE = os.path.join(LOG_BASE_DIR, "logs", "base_img").replace('\\', '/')
# 测试报告目录
TEST_REPORT = os.path.join(LOG_BASE_DIR, "logs", "report").replace('\\', '/')
# 日志目录
LOG_DIR = os.path.join(LOG_BASE_DIR, "logs", "pylog").replace('\\', '/')
# 测试数据文件
TEST_DATA = os.path.join(BASE_DIR, "myConfig", "keyword.xls")
# 元素控件
TEST_ELEMENT_DIR = os.path.join(BASE_DIR, "myConfig", "LocalElement.ini")
# 键盘
KEY_PAD = os.path.join(BASE_DIR, "myConfig", "keypad.ini")
# 配置执行那些测试用例
CASELIST_DIR = os.path.join(BASE_DIR, "myConfig", "zouchaCaseList.txt")
