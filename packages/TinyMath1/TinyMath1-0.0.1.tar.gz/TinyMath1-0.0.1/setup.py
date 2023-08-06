'''
Setup for the ssv package
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='TinyMath1',
    version="0.0.1",
    author='Ray Seikel',
    author_email='rseikel@bigpond.com',
    description='A small mathematics library',
    long_description=long_description,
    url="https://github.com/einshoe/TinyMath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
