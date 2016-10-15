# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
__version__ = '0.0.1'
install_requires = []

setup(
    name="ebbinghaus_calendar",
    version=__version__,
    license='Proprietary',
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    description="A calendar service by Ebbinghaus rule",
    long_description="A calendar and reminder App",
    author="jiao.xue",
    author_email="jiao.xuejiao@gmail.com",
    keywords=("appcategory", "egg"),
    install_requires=install_requires,
    platforms="any",
    entry_points={},
)
