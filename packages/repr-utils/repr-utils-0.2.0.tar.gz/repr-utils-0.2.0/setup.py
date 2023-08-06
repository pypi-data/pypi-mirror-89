# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['repr_utils', 'repr_utils.templates']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.1,<3.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'repr-utils',
    'version': '0.2.0',
    'description': 'Contains common elements that when displayed will adhere to the correct format (e.g markdown, latex, html, text) in tools like jupyter notebooks',
    'long_description': '.. image:: https://github.com/luttik/repr_utils/workflows/CI/badge.svg\n    :alt: actions batch\n    :target: https://github.com/Luttik/repr_utils/actions?query=workflow%3ACI+branch%3Amaster\n.. image:: https://badge.fury.io/py/repr-utils.svg\n    :alt: pypi\n    :target: https://pypi.org/project/repr-utils/\n\n.. image:: https://codecov.io/gh/luttik/repr_utils/branch/master/graph/badge.svg\n    :alt: codecov\n    :target: https://codecov.io/gh/luttik/repr_utils\n\nREPR-UTIL\n---------\nA toolkit to quickly display elements in tools like `jupyter`_ by building upon `ipython rich display`_.\n\nContains simple objects that will automatically be converted to the right format based on the context.\n\nInstallation\n============\nRun :code:`pip install repr-utils`\n\nExamples\n========\nLook at `the examples notebook`_\n\nSupports:\n=========\n- Plain Text\n- HTML\n- Markdown\n- Latex\n\nCurrent objects:\n================\n- Header\n- Table\n- Lists\n\nRelevant links:\n===============\n- `pypi`_\n- `github`_\n\nContributions are appreciated.\n\n.. _`the examples notebook`: examples.ipynb\n.. _`pypi`: https://pypi.org/project/repr-utils/\n.. _`github`: https://github.com/Luttik/repr_utils/\n.. _`ipython rich display`: https://ipython.readthedocs.io/\n.. _`jupyter`: https://jupyter.org/\n',
    'author': 'luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luttik/repr_utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
