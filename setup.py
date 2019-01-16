"""
setup.py for svnlab
"""

import os
from setuptools import find_packages, setup

# Document:
# [1] https://setuptools.readthedocs.io/en/latest/setuptools.html
# [2] https://www.cnblogs.com/numbbbbb/p/3615155.html
# [3] http://blog.konghy.cn/2018/04/29/setup-dot-py/

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# 第三方依赖包及版本
requires = [
    'django>=2.0.9',
    'django-cors-headers>=2.4.0',
    'djangorestframework>=3.9.0',
    'mysqlclient>=1.3.14',
    'Pillow>=5.4.1',
    'docutils>=0.3',
    'python-ldap>=3.1.0',
]

# setuptools [1]
setup(
    name='svnlab',
    version='1.0',
    packages=find_packages(),
    # package_dir = {'': 'svnlab'}
    # scripts 参数是一个 list，安装包时在该参数中列出的文件会被安装到系统 PATH 路径下
    # scripts=['svnlab/manage.py'],

    # entry_points 参数用来支持自动生成脚本，其值应该为是一个字典，从 entry_point 组名映射到一个表
    # 示 entry_point 的字符串或字符串列表 [3]
    # entry_points = {'console_scripts': [
    #     'svnlab-manage = svnlab.manage:main',
    # ]},

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=requires,

    # use MANIFEST.in [2]
    # 该参数被设置为 True 时自动添加包中受版本控制的数据文件，可替代 package_data，同时，
    # exclude_package_data 可以排除某些文件。注意当需要加入没有被版本控制的文件时，还是仍然需要使用
    # package_data 参数才行
    include_package_data=True,
    # exclude_package_data={
    #     '': ['.gitignore']
    # },
    # package_data = {
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },
    # data_files=[
    #     ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #     ('config', ['cfg/data.cfg']),
    #     ('/etc/init.d', ['init-script'])
    # ],

    license='MIT License',
    keywords="svnlab",
    description='A simple Django app to manage svn server.',
    long_description=README,
    url='https://github.com/jiuchou/svnlab',
    author='jiuchou',
    author_email='315675275@qq.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    project_urls={
        "Bug Tracker": "https://github.com/jiuchou/svnlab/issues",
        "Documentation": "https://github.com/jiuchou/svnlab/wiki",
        "Source Code": "https://github.com/jiuchou/svnlab",
    }
)
