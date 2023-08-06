import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ytimg",
    version="1.1",
    author="Potatochips2001",
    author_email="",
    description="Gets thumbail of a Youtube video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Potatochips2001/ytimg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)