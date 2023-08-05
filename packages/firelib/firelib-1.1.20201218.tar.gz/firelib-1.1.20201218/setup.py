
from setuptools import setup, find_packages
from time import localtime,strftime
vi="1.1"
day=1
loacl=strftime(f"%Y%m%d",localtime())
setup(
    name='firelib',
    version=f"{vi}.{loacl}",
    description=(
        '🔥火焰爱搜🔥学而思专用库🔥'
    ),
    long_description=open('README.md',encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='asunc',
    author_email='hychat@asunc.cn',
    maintainer='asunc',
    maintainer_email='hychat@asunc.cn',
    license='BSD License',
    packages=find_packages(exclude=["firelib.__init__", "firelib.api", "firelib.hychat", "firelib.qq","firelib.xes"]),
    platforms=["all"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=['requests','json',"xingyunlib","huoyanlib"]
)
#
# 9abe5372d54460c07f202585e7da2cf53cf016bc884542732e07a3544275"""