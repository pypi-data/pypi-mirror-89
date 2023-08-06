import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'term_math'
AUTHOR = 'Bhavin Gala'
AUTHOR_EMAIL = 'bhavinpgala@gmail.com'
URL = 'https://github.com/bgala/term_math'

LICENSE = 'MIT License'
DESCRIPTION = 'Add, subtract, multiply, divide with terminal'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"


setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      packages=find_packages()
      )