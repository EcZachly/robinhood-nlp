import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robinhood-scraper-nlp",
    version="0.0.2",
    author="Zachary Wilson",
    author_email="zachwilson130@gmail.com",
    description="A package that interacts with Robinhood APIs to access news about stocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EcZachly/robinhood-nlp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)