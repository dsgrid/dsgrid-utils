import setuptools
import pathlib

here = pathlib.Path(__file__).parent

with open(here / 'dsgflex' / '_version.py', encoding='utf-8') as f:
    version = f.read()

version = version.split()[2].strip()[2].strip('"')

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setuptools.setup(
    name = 'dsgutils',
    version = version,
    author = 'Elaine Hale',
    author_email = 'elaine.hale@nrel.gov',
    packages = setuptools.find_packages(),
    python_requires = '>=3.6',
    description = 'Python package of functionality used in both dsgrid-load and dsgrid-flex',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    install_requires=[
        'numpy',
        'pandas'
    ],
    extras_require={
    }
)
