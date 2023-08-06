#import pathlib
from os import path
from setuptools import setup ,find_packages

# The directory containing this file
#HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    README = f.read()

# This call to setup() does all the work
setup(
    name="pix_apidata",
    version="1.2.2",
    packages=['pix_apidata'],
    description="Python library to connect and stream the market data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pscoumar",
    author="Coumar Pandourangane",
    author_email="pscoumar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    keywords = 'stock market, apidata, accelpix, ticanalytics',
    include_package_data=True,
    install_requires=['signalrcore-async', 'urllib3'],
    python_requires=">=3.7",

)