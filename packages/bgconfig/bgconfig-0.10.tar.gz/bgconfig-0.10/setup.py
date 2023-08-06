from setuptools import setup

__version__ = '0.10'
__author__ = 'Jordi Deu-Pons'
__author_email__ = 'jordi.deu@irbbarcelona.org'

setup(
    name="bgconfig",
    version=__version__,
    install_requires=['configobj >= 5.0.6', 'appdirs >= 1.4.3'],
    author=__author__,
    author_email=__author_email__,
    description="Bgconfig library to manage configuration files.",
    license="Apache License 2",
    keywords="",
    url="https://bitbucket.org/bgframework/bgconfig",
    download_url="https://bitbucket.org/bgframework/bgconfig/get/"+__version__+".tar.gz",
    include_package_data=True,
    zip_safe=True,
    py_modules=['bgconfig']
)
