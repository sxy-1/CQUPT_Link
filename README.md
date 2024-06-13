<p align="center">
  <img width="18%" align="center" src="https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202312262148798.png" alt="logo">
</p>
  <h1 align="center">
  重邮校园网客户端登录
</h1>
<p align="center">
  基于 PyQt6 - Fluent Design 设计
</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win-blue?color=#4ec820" alt="Platform Win"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
    </a>
    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/version-2.0.1-blue?color=#4ec820" alt="v2.0.1"/>
  </a>
</p>



### 介绍

本程序基于pyqt6开发，使用pyqt6-fluent-widgets美化组件，提供重邮校园网伪装设备类型，gui登录等。

![image-20240606140255392](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406061402629.png)

### 功能

- [x] 电脑端/移动端切换

- [x] 通过伪装，支持双电脑同时在线

- [x] 特殊登录？

- [ ] 突破坑位限制-不支持



### 项目结构

```
|----account.db         sqlite3数据库 如果没有自动生成
|----change_mac_csdn.py 修改mac
|----config.json        设置间隔时间、编码
|----config.py          配置文件处理
|----ConnectDb.py       连接数据库程序
|----connect_wifi.py    连接wifi
|----CQUPT_Link.py      主程序
|----Get_local_ip.py    获取有线/无线的本地ip
|----images.py			使用pyrcc5转换图片
|----images.qrc			使用pyrcc5转换图片
|----is_admin.py		转为管理员身份运行
|----LICENSE			GPL-3.0 license
|----log\				日志文件
|----Logger.py			日志处理
|----LoginWindow.py		登录界面
|----Logout.py			校园网注销
|----pyrcc5.exe  		pyrcc5处理图片
|----README.md			README
|----requirements.txt 	依赖，可能有冗余
|----resource\			资源文件
|----untitled.ui		源ui
|----zifuwu.py			打开自服务

```



### 自编译

如果您想自行编译源码，在导入requirements后
```
pyinstaller -w -i .\resource\images\favicon.ico CQUPT_Link.py
```



### 使用须知

特殊登录仅供学习交流。

特殊登录在按下登录按钮后不会有任何显示，直到约1分钟后显示结果，期间请不要对本程序有任何操作，若强制关闭导致wifi驱动下线，请自行在设备管理器重新开启/重装wifi驱动。

再次强调，需要静等一分钟，直至出现弹窗。

若有任何bug，请提交issue或直接与作者联系。





## 其他

我们目前需要更多朋友们帮我们完善该程序。

- 当前config.json的间隔时间不稳定，需要更多测试。

- 登录过程无法正常显示进度条。

- 没有网速测速模块。

- 无法python模拟dhcp请求。

如果您可以提供代码上的帮助，欢迎与我们联系，万分感谢。



### 参考

[校园网自动登录全平台解决方案 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/364016452?utm_medium=social&utm_oi=1112727310867927040&utm_id=0)



### 许可证

CQUPT_Link 使用 GPLv3 许可证.

Copyright © 2023 by dullspear

