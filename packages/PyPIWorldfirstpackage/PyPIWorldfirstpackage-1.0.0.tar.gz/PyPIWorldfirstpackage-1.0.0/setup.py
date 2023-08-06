from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='PyPIWorldfirstpackage',

    version='1.0.0',

    

    long_description=long_description,

    long_description_content_type='text/markdown',

    author='Andrii Bessarab',

    author_email='andriibessarab@gmail.com',

    

    packages=find_packages(),

)