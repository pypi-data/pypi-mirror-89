# coding:utf-8


from setuptools import setup

# or
# from distutils.core import setup

setup(
    name='my-vic-009',  # 包名字
    version='1.0',  # 包版本
    description='学习打包',  # 简单描述
    author='vic',  # 作者
    author_email='vic@163.com',  # 作者邮箱
    url='https://www.vic.com',  # 包的主页
    packages=['vic_pkg','tests'],  # 包
    package_data={'vic_pkg': ['*.ini']}
)
