import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydotmap",
    version="0.0.3",
    author="Atul Kumar Singh",
    author_email="atulsingh0401@gmail.com",
    description="Dot notation python dicationary",
    long_description="""# pydotmap
[![built with Python3](https://img.shields.io/badge/built%20with-Python3.x-red.svg)](https://www.python.org/)
### This package is just a wrapper to python standard library `dict`. It will allow you to use python dict or dictionary as dot notation just like javascript object. You can use simple and complex dict with this library. <br><br>

### How to use?

```
from pydotmap import DotMap


author = DotMap(name="atul", sirname="singh", addr=[{"country": "India"}])
print(author.name)
print(author.sirname)
del author.sirname
print(author.sirname)
print(author.get("sirname", "singh"))  # you can use your default value same as dict
print(author.addr[0].country)
```

""",
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
