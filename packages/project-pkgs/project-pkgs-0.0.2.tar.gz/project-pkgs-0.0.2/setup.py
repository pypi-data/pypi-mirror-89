'''
Date: 2020-12-22 11:29:49
LastEditors: Rustle Karl
LastEditTime: 2020-12-22 14:08:33
'''
import os.path

from setuptools import setup

'''
python setup.py sdist
pip install dist/project-pkgs-0.0.2.tar.gz
python setup.py bdist_wheel
pip install twine
twine upload dist/*
'''

# What packages are required for this module to be executed?
requires = [
    # 'requests',
]

# Import the README and use it as the long-description.
cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='project-pkgs',
    py_modules=['color'],  # 给文本添加颜色
    packages=['logger'],
    version='0.0.2',
    license='BSD',
    author='Rustle Karl',
    author_email='fu.jiawei@outlook.com',
    description='个人项目常用库',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['color', 'logger', 'pkgs'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=requires,
)
