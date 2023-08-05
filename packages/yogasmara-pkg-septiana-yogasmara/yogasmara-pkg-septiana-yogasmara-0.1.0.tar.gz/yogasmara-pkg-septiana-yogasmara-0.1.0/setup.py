import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'yogasmara-pkg-septiana-yogasmara'
AUTHOR = 'Septiana Yogasmara'
AUTHOR_EMAIL = 'septianayoga30@gmail.com'
URL = 'https://github.com/yoga1234/yogasmara-addon'

LICENSE = 'MIT License'
DESCRIPTION = 'Yogasmara Python script build for blender'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = []

setup(
  name=PACKAGE_NAME,
  version=VERSION,
  author=AUTHOR,
  author_email=AUTHOR_EMAIL,
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  long_description_content_type=LONG_DESC_TYPE,
  url=URL,
  packages=find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ]
)