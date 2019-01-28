# Windows中类似Linux的grep和which命令替代者findstr和where

## 1. 前言
因为在Linux环境中工作多年，早已习惯常用的命令。现如今切换到Windows下工作，诸多不便，其中which和grep就是其中之二，希望能帮助有同样疑惑的朋友。

## 2. grep替代者find/findstr

grep使用实在太频繁了，比如查询当前正在运行的程序
```
ps -ef | grep java
```

windows提供find/findstr类似命令，其中findstr要比find功能更多一些，可以/?查看帮助。
```
## CMD
C:\Users\kigao>find /N "SELECT" .\xiaomi.sql

---------- .\XIAOMI.SQL
[1]SELECT XmSysConfigEO.SYSCONFIG_ID,

C:\Users\kigao>netstat -an|find "1521"
  TCP    0.0.0.0:1521           0.0.0.0:0              LISTENING
  TCP    [::]:1521              [::]:0                 LISTENING
  TCP    [::1]:1521             [::1]:49685            ESTABLISHED
  TCP    [::1]:49685            [::1]:1521             ESTABLISHED

## PS
PS C:\Users\kigao> tasklist | findstr /i wox
Wox.exe                       9732 Console                    2    174,332 K

```
要注意的是，find查找的字符串必须带双引号，而findstr不需要。
要注意的是在PowerShell中find无法使用，所以我一般使用findstr，比如查询是否已安装virtualenv。
```
PS C:\Users\kigao> pip list | findstr virtu
virtualenv             16.3.0
```

## 3. which替代者where/Get-Command

因为电脑很多环境，命令也有多个版本，很多时候需要查看一下当前默认命令路径，Linux中使用which，windows中也有where来替代。
```
#CMD
C:\Users\kigao>where cmd
C:\Windows\System32\cmd.exe
```
当然如果批处理比较熟悉的朋友也能在cmd中写个循环来查询命令
```
C:\Users\kigao>for %x in (pip.exe) do @echo %~$PATH:x
D:\Program Files\Python3.7\Scripts\pip.exe
```
要注意的是在PS中，因为where是Where-Object的别名，所以需要使用“where.exe”。
```
PS C:\Users\kigao> where.exe cmd
C:\Windows\System32\cmd.exe
```
同时，PS也提供了Get-Command命令实现类似功能
```
PS C:\Users\kigao> Get-Command cmd

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Application     cmd.exe                                            10.0.16... C:\WINDOWS\system32\cmd.exe

PS C:\Users\kigao> Get-Command where

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           where -> Where-Object

PS C:\Users\kigao> Get-Command where.exe

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Application     where.exe                                          10.0.16... C:\WINDOWS\system32\where.exe
```
因为命令太长，还是惯于使用“where.exe”。

## 4. 结语
如有疑问，欢迎留言共同探讨。