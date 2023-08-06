#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Administrator
@file: setup.py
@time: 2020/12/24
@desc:
"""


from distutils.core import setup
# distutils 指归档文件包

setup(
    name='CS_2000_childhood',  # 对外这个模块的名字
    version='1.1',  # 版本号
    description='这是为纪念小时候玩的CS游戏射击游戏而开发的小游戏。仅做测试',  # 描述
    author='Minsky',  # 作者
    author_email='fake_email_notry@qq.com',  # 联系方式
    py_modules=['CS_2000_childhood.accelerate', 'CS_2000_childhood.picture_download']  # 填写发布的模块。便 CS包 文件夹下有其他模块文件，不发布也不用写，
    # 后面的 python setup.py sdist 命令只会打包要发布的模块。
)
