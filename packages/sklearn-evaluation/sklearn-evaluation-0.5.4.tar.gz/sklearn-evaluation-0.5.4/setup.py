import re
import ast
from setuptools import setup, find_packages
from glob import glob
from os.path import splitext
from os.path import basename

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/sklearn_evaluation/__init__.py', 'rb') as f:
    VERSION = str(
        ast.literal_eval(
            _version_re.search(f.read().decode('utf-8')).group(1)))

DOWNLOAD_URL = ('https://github.com/edublancas/sklearn-evaluation/tarball/{}'.
                format(VERSION))

DOCS = [
    'sphinx',
    'ipython',
    'sphinx-rtd-theme',
    'ploomber',
    'nbsphinx',
    'seaborn',
    # to display progress bar when executing notebooks using papermill
    # in NotebookCollection.py example
    'ipywidgets'
]

TEST = [
    'jupytext',
    'papermill',
    'ipykernel',
    'pytest',
    # need to pin this version because pytest 4 breaks matplotlib image
    # comparison tests
    'pytest-cov',
    # for coveralls.io
    'coveralls',
]

DEV = [
    'flake8',
    'yapf',
]

ALL = DOCS + TEST + DEV

setup(name='sklearn-evaluation',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      version=VERSION,
      description=('scikit-learn model evaluation made easy: plots, tables and'
                   'markdown reports.'),
      url='http://github.com/edublancas/sklearn-evaluation',
      download_url=DOWNLOAD_URL,
      author='Eduardo Blancas Reyes',
      author_email='github@blancas.io',
      license='MIT',
      keywords=['datascience', 'machinelearning'],
      classifiers=[],
      include_package_data=True,
      install_requires=[
          'scikit-learn',
          'matplotlib',
          'decorator',
          'jinja2',
          'tabulate',
          'mistune',
          'pandas',
          'nbformat',
      ],
      extras_require={
          'all': ALL,
      })
