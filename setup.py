from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8", errors="ignore") as fh:
    long_description = fh.read()

setup(
    name='nonebot_plugin_bfinfo',      # 这里是pip项目发布的名称
    version='0.0.5',  # 版本号，数值大的会优先被pip
    keywords = ["pip", "nonebot2", "nonebot", "battlefield", "nonebot_plugin"],
    description = "nonebot plugin bfinfo",
    long_description = long_description,
    # long_description = "An feature extraction algorithm, improve the FastICA",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    url = "https://github.com/GC-ZF/nonebot_plugin_bfinfo",     # 项目相关文件地址，一般是github
    author = "zhangshier",
    author_email = "1310446718@qq.com",

    packages = find_packages(), # 系统自动从当前目录开始找包
    # 如果有的文件不用打包，则只能指定需要打包的文件
    #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀

    python_requires=">=3.7.3,<4.0",
    include_package_data = True,
    platforms = "any",

    install_requires=[
        'nonebot2>=2.0.0-beta.4',
        'nonebot-adapter-onebot>=2.0.0-beta.1',
        'matplotlib>=3.6.2',
        'Pillow>=9.3.0',
        'requests>=2.28.1'
    ]
)
