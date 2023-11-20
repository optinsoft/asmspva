from distutils.core import setup
import re

s = open('asmspva/version.py').read()
v = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", s, re.M).group(1)

setup(name='asmspva',
    version=v,
    description='Async API wrapper for smspva',
    install_requires=["aiohttp","certifi"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['smspva','sms','async'],
    url='https://github.com/optinsoft/asmspva',
    packages=['asmspva']
)