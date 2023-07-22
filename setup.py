import setuptools

requirements = ['numpy']  # 自定义工具中需要的依赖包

setuptools.setup(
    name="WaterScenes",  # 自定义工具包的名字
    version="1.0.2",  # 版本号
    author="Shanliang Yao",  # 作者名字
    author_email="shanliang.yao19@gmail.com",  # 作者邮箱
    description="Toolkit for WaterScenes",  # 自定义工具包的简介
    license='MIT-0',  # 许可协议
    url="https://github.com/waterscenes",  # 项目开源地址
    packages=setuptools.find_packages(),  # 自动发现自定义工具包中的所有包和子包
    install_requires=requirements,  # 安装自定义工具包需要依赖的包
    python_requires='>=3.8'  # 自定义工具包对于python版本的要求
)
