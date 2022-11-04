from setuptools import setup, find_packages


# Package meta-data.
NAME = 'eurobonus-to-mmex-csv'
DESCRIPTION = 'Eurobonus transactions CSV to Money Manager Ex transactions converter.'
URL = 'https://github.com/moisesber/eurobonus-to-mmex-csv'
EMAIL = 'moisesber@gmail.com'
AUTHOR = 'Moises Rodrigues'
REQUIRES_PYTHON = '>=3.9.0'
VERSION = '0.0.1' 
LICENSE = 'MIT'
# What packages are required for this module to be executed?
REQUIRED = [
      #'csv', 're',
      'Click',
]


about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'mmex-csv-generator = app.cli:cli',
        ],
    },
)

