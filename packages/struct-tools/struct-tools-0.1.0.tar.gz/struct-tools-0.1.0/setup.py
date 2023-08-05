# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['struct_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'struct-tools',
    'version': '0.1.0',
    'description': 'Attribute-access and align-printed dicts.\nTransposing dict-of-dicts, list-of-lists, and mixed.\nDeep (nested) attribute access.\nPrint functionality also provided as class to be subclassed.\nDict intersection, complement.\nCartesian product.\n',
    'long_description': '# struc-tools\n\nTools for working with data containers/structures,\ni.e. lists, dicts, classes.\n\n### TODO\nSee alternatives:\n- <https://github.com/srevenant/dictlib>\n- <https://pypi.org/project/dict/>\n- <https://pypi.org/project/dicty/>\n- <https://pypi.org/project/print-dict/>\n- <https://pypi.org/project/dictionaries/>\n\nAnswer SO.com questions:\n<https://www.google.com/search?q=python+aligned+dict&oq=python+aligned+dict>\n',
    'author': 'patricknraanes',
    'author_email': 'patrick.n.raanes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
