import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazynumpy",
    version="0.0.1",
    author="Kenneth S Goodman",
    author_email="kennethsgoodman@yahoo.com",
    description="A wrapper around numpy that does lazy evaluations to optimize for chained matrix multiplication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kennethgoodman/lazynumpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
