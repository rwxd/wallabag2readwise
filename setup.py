from setuptools import setup
from os import path

with open("./requirements.txt") as f:
    required = f.read().splitlines()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wallabag2readwise',
    version='0.1.0',
    description='Push wallabag annotations to Readwise highlights',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rwxd',
    author_email='rwxd@pm.me',
    url="https://github.com/rwxd/wallabag2readwise",
    license='MIT',
    packages=['wallabag2readwise'],
    install_requires=required,
    entry_points={
        "console_scripts": ["wallabag2readwise = wallabag2readwise.__main__:main"]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
