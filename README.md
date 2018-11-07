# OKEXFutureQuickAccess
用于OKEX合约的快捷键工具

# 初次运行

运行前请确保已安装 Python 3.5+ 版本
在控制台中输入`pip3 install websocket-client requests keyboard`安装程序使用的必要环境。

初次运行需要设置API密钥，在 [OKEX](https://www.okex.com/account/users/myApi) 获取密钥 ，在apiconfig.py中填写`APIKEY`及`APISECRET`字段。默认的仓位大小比较激进，请按自身需求修改`SIZE`字段。

# 快捷键设置
默认快捷键为 开多(OPEN_LONG) F1; 开空(OPEN_SHORT) F2; 平多(COVER_LONG) ALT+F1; 平空(COVER_SHORT) ALT+F2; 多空全平(COVER_ALL) ALT+\`; 取消所有未完成订单(CANCEL_ALL_PENDING) ESC. 修改快捷键需要修改`main.py`文件进行更改。
