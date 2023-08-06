import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydotmap",
    version="0.0.2",
    author="Atul Kumar Singh",
    author_email="atulsingh0401@gmail.com",
    description="Dot notation python dicationary",
    long_description="This package is just a wrapper to python standard library `dict`. It will allow you to use python dict or dictionary as dot notation just like javascript object. You can find the source code here https://github.com/iamatulsingh/pydotmap/",
    long_description_content_type="text/markdown",
    url="https://github.com/iamatulsingh/pydotmap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)