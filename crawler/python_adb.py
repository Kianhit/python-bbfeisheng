import os
import re

# print(os.system('adb version'))
# print(os.system('adb --help'))
# print(os.system('adb shell "dumpsys activity | grep "mFocusedActivity""'))
# out = os.popen('adb shell "dumpsys activity | grep "mFocusedActivity""').read()
# print(os.system('adb devices'))

# os.system('adb version')
# os.system('adb devices')  # os.system是不支持读取操作的
# os.popen支持读取操作
# out = os.popen('adb shell "dumpsys activity | grep "mFocusedActivity""').read()
# print(out)

# 下面的代码是获取当前窗口的component参数


def getFocusedPackageAndActivity():

    # 这里使用了正则表达式，对输出的内容做了限制，只会显示类似"com.mediatek.factorymode/com.mediatek.factorymode.FactoryMode"的字符串
    pattern = re.compile(r"[a-zA-Z0-9\.]+/[a-zA-Z0-9\.]+")
    # window下使用findstr
    out = os.popen(
        r"adb shell dumpsys window windows | findstr \/ | findstr name=").read()
    list = pattern.findall(out)
    component = list[0]  # 输出列表中的第一条字符串

    return component


print(getFocusedPackageAndActivity())
