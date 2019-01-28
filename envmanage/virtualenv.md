# Python步步飞升之virtualenv

## 1. virtualenv介绍
virtualenv用于创建python多环境，这些环境是相互独立的，特别适合当有多个项目，每个项目引用不同的库包，甚至同库包不同版本的情况，保障每个项目都有一个独立的环境。

## 2. virtualenv安装
可以使用源码安装或使用pip安装，推荐使用pip安装。
```
PS C:\Users\kigao> pip install virtualenv
Collecting virtualenv
  Downloading https://files.pythonhosted.org/packages/8f/f1/c0b069ca6cb44f9681715232e6d3d65c75866dd231c5e4a88e80a46634bb
/virtualenv-16.3.0-py2.py3-none-any.whl (2.0MB)
    100% |████████████████████████████████| 2.0MB 1.1MB/s
Requirement already satisfied: setuptools>=18.0.0 in d:\program files\python3.7\lib\site-packages (from virtualenv) (39.
0.1)
Installing collected packages: virtualenv
Successfully installed virtualenv-16.3.0
```

## 3. 创建虚拟环境
我这里指定了python2.7为解释器，如果不用“-p”参数，则为系统默认python.exe
```
PS D:\Program Files\PythonVirtualEnvs> virtualenv -p "D:\Program Files\Python2.7\python.exe" proj1
Running virtualenv with interpreter D:\Program Files\Python2.7\python.exe
New python executable in D:\Program Files\PythonVirtualEnvs\proj1\Scripts\python.exe
Installing setuptools, pip, wheel...
done.
```
同时，如果带上“--system-site-packages”参数，会将相应环境的包继承到新创建的虚拟环境中。
```
virtualenv --system-site-packages proj1
```
命令执行后，会在当前目录下，建立了一个“proj1”文件夹
```
PS D:\Program Files\PythonVirtualEnvs> ls

    Directory: D:\Program Files\PythonVirtualEnvs

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2019/1/28     15:21                proj1
```
proj1内部创建了Include，Lib和Scripts文件夹。
从[virtualenv官网](https://virtualenv.pypa.io/en/latest/userguide/#usage)可知：
- “ENV/lib/”和“ENV/include/”是支持相关的库文件目录，后期安装的包会放在“ENV/Lib/[pythonX.X/]site-packages/”中。
- “ENV/bin”就是放可执行文件的，比如说python，pip，在windows中名为““ENV/Scripts”
```
PS D:\Program Files\PythonVirtualEnvs\proj1> ls

    Directory: D:\Program Files\PythonVirtualEnvs\proj1

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2018/5/23     10:05                Include
d-----        2019/1/28     15:21                Lib
d-----        2019/1/28     15:22                Scripts
```
可以看到虚拟环境中python为2.7.15版本，不同于系统默认的3.7.0版本
```
PS D:\Program Files\PythonVirtualEnvs\proj1> python -V
Python 3.7.0
PS D:\Program Files\PythonVirtualEnvs\proj1> .\Scripts\python.exe -V
Python 2.7.15
```
现在可以在命令行中运行“Scripts\activate”的bat(针对CMD)或者ps1(针对PS)来激活当前环境
```
PS D:\Program Files\PythonVirtualEnvs\proj1\Scripts> .\activate.ps1
(proj1) PS D:\Program Files\PythonVirtualEnvs\proj1\Scripts> cd ..
(proj1) PS D:\Program Files\PythonVirtualEnvs\proj1> python -V
Python 2.7.15
```
可以看到左边“(proj1)”代表当前使用proj1虚拟环境。
关闭窗口或者运行“Scripts\deactivate用以退出虚拟环境。

## 4. 在VS Code中使用virtualenv建立的虚拟环境
盖因习惯于使用VS Code，其它IDE请查看相关资料，主要思路就是添加虚拟环境中python.exe作为默认。
编辑项目中.vscode/settings.json文件
```
{
    // "python.pythonPath": "D:\\Program Files\\Python3.7\\python.exe"
    "python.pythonPath": "D:\\Program Files\\PythonVirtualEnvs\\proj1\\Scripts\\python.exe"
}
```
重启VS Code，然后可以看到左下角显示当前Python执行环境，同时点击之后可以随意切换。
![左下角查看当前Python执行环境](https://github.com/Kianhit/python-bbfeisheng/raw/master/envmanage/virtualenv_vscode_1.png)
这样，我右键选择“在当前终端执行Python文件”命令时，终端中显示的Python.exe已切换为虚拟环境
```
PS C:\Users\kigao\Documents\code\python-bbfeisheng> & "D:/Program Files/PythonVirtualEnvs/proj1/Scripts/python.exe" c:/Users/kigao/Documents/code/python-bbfeisheng/collections/note_ChainMap.py
```

## 5. 删除虚拟环境
简单的deactivate，然后删除环境目录
```
(proj1) PS D:\Program Files\PythonVirtualEnvs\proj1> deactivate
PS D:\Program Files\PythonVirtualEnvs> rm proj1 -recurse
```
## 6. 结语
如有疑问，欢迎留言共同探讨。