import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    # 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    name="enta",
    # 程序版本
    version="0.0.1",
    # 项目作者
    author="ireman",
    # 作者邮件
    author_email="z_fsong@163.com",
    # 项目的一句话描述
    description="Excel数字转列字母",
    # 加长版描述？
    long_description=long_description,
    # 描述使用Markdown
    long_description_content_type="text/markdown",
    # 项目地址
    url="",
    # 无需修改
    packages=setuptools.find_packages(),
    classifiers=[
        # 使用Python3
        "Programming Language :: Python :: 3",
        # 开源协议
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
