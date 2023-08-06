import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libkget", 
    version="0.1.1",
    author="kalekale",
    author_email="kalekale.anon@gmail.com",
    description="Simple library to download files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0kalekale/libkget",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)