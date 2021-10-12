# Author: Third Musketeer
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name='pavlok',
    version='0.1.4',
    license='MIT',
    author="Maneesh Sethi",
    author_email='maneesh@pavlok.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Pavlok/pavlok-python-client',
    keywords='pavlok',
    include_package_data=True,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        "Authlib==0.15.4",
        "fastapi==0.68.1",
        "pydantic==1.8.2",
        "starlette==0.14.2",
        "uvicorn==0.15.0",
        "httpx==0.19.0",
        "itsdangerous==2.0.1",
        "python-dotenv==0.19.0",
        "Jinja2==3.0.1"
      ],

)
