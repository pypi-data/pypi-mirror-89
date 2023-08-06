import pathlib
from setuptools import setup, find_packages

HERE    = pathlib.Path(__file__).parent
README  = (HERE/'README.md').read_text()

setup(
    name='tebula',
    version='0.0.0',
    description='Tabular Langauge',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Durga Datta Kandel, Yashoda Neupane',
    author_email='dindefi@gmail.com',
    license='Apache 2.0',
    include_package_data=True,
    # Dict[Package Name, Dir Name]
    package_dir={'m ': 'src'},
    packages=find_packages(exclude=['tests']),
)
