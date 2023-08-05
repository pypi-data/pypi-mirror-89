import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MiniWordTools",
    version="0.0.1",
    author="Ying Liqian",
    author_email="jamesylq@gmail.com",
    description="A library with tools for strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ajayff4/testing2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

