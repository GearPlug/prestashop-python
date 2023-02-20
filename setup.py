import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="prestashop-python",
    version="0.1.1",
    description="API wrapper for Prestashop written in Python",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/GearPlug/prestashop-python",
    author="Juan Carlos Rios",
    author_email="juankrios15@gmail.com",
    license="MIT",
    packages=["prestashop"],
    install_requires=[
        "requests",
    ],
    zip_safe=False,
)
