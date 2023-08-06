import pathlib
import re

from setuptools import setup, find_packages

WORKING_DIR = pathlib.Path(__file__).parent


def read(f):
    return (WORKING_DIR / f).read_text('utf-8').strip()


def get_version():
    init_py = (WORKING_DIR / "botapi" / "__init__.py").read_text("utf-8")
    try:
        return re.findall(r'^__version__ = "([^"]+)"\r?$', init_py, re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


setup(
    name='botapi',
    version=get_version(),
    packages=find_packages(),
    url='https://github.com/EdiBoba/botapi',
    license='Apache 2.0',
    author='Vyacheslav Rineisky',
    author_email='rineisky@gmail.com',
    description="Library for build json API's",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Operating System :: OS Independent'
    ),
    include_package_data=True
)
