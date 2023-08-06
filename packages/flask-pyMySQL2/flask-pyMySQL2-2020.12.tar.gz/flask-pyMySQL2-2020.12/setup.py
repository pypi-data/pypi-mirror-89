# -*- coding: UTF-8 -*-
from setuptools import setup


setup(
    name="flask-pyMySQL2",
    version="2020.12",
    url="https://github.com/livermorium/flask-mysql.git",
    license="MIT",
    author="livermorium",
    description="Flask simple mysql client",
    packages=["flask_pymysql"],
    namespace_packages=["flask_pymysql"],
    zip_safe=False,
    platforms="any",
    install_requires=["Flask", "PyMySQL"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
