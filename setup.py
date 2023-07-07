from distutils.core import setup

setup(name='asmspva',
    version='1.0',
    description='Async API wrapper for smspva',
    install_requires=["aiohttp","certifi"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['smspva','sms','async'],
    url='https://github.com/optinsoft/asmspva',
    packages=['asmspva']
)