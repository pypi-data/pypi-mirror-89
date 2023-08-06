from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aiomangadexapi",
    version="1.1.0",
    author="Mudy7",
    author_email = "retaketurbo@gmail.com",
    description="An asychronous mangadex API wrapper with updates and more!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mudy7/aiomangadexapi",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["feedparser", "aiohttp","lxml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
