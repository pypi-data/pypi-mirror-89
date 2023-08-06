import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hun-date-parser-nsoma97",
    version="0.0.1",
    author="Soma Nagy",
    author_email="nagysomabalint@gmail.com",
    description="A tool for extracting datetime intervals from Hungarian sentences and turning datetime objects into Hungarian text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nsoma97/hun-date-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
