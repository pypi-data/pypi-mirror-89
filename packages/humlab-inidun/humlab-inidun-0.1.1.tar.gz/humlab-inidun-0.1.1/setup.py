# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notebooks',
 'notebooks.co_occurrence',
 'notebooks.common',
 'notebooks.pos_statistics',
 'notebooks.word_trends']

package_data = \
{'': ['*']}

install_requires = \
['bokeh',
 'click',
 'ftfy',
 'gensim',
 'glove-python-binary>=0.2.0,<0.3.0',
 'humlab-penelope>=0.2.35,<0.3.0',
 'ipyaggrid',
 'ipyfilechooser>=0.4.0,<0.5.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'jupyter',
 'jupyter-bokeh>=2.0.4,<3.0.0',
 'jupyterlab',
 'matplotlib',
 'memoization',
 'nltk',
 'pandas',
 'pandas-bokeh>=0.5.2,<0.6.0',
 'pandocfilters==1.4.2',
 'qgrid>=1.3.1,<2.0.0',
 'sidecar>=0.4.0,<0.5.0',
 'spacy',
 'textacy',
 'tqdm>=4.51.0,<5.0.0',
 'wordcloud']

setup_kwargs = {
    'name': 'humlab-inidun',
    'version': '0.1.1',
    'description': 'INIDUN research project text analysis tools and utilities',
    'long_description': '# The INIDUN Text Analytics Repository\n\n### Prerequisites\n\n### Installation\n\n### Note\n\n\n',
    'author': 'Roger Mähler',
    'author_email': 'roger.mahler@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://inidun.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
