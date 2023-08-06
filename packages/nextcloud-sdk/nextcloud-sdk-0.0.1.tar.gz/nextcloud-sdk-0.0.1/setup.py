from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nextcloud-sdk',
    version="0.0.1",
    author='CookCoder',
    author_email='zhangrcheng@gmail.com',
    description="A python implementation of nextcloud API.",
    packages=find_packages(),
    python_requires='>=3.6',
)