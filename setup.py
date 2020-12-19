import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bookstore",
    version="1.0.0",
    author="mathskiller",
    author_email="chennuo909@163.com",
    description="Buy Books Online",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1012598167/bookstore.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
