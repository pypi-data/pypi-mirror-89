# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_cube']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xarray-cube',
    'version': '0.1.0',
    'description': 'xarray extension for spectral cube analysis',
    'long_description': '# xarray-cube\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-cube.svg?label=PyPI&style=flat-square)](https://pypi.org/project/xarray-cube/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-cube.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/xarray-cube/)\n[![Test](https://img.shields.io/github/workflow/status/a-lab-nagoya/xarray-cube/Test?logo=github&label=Test&style=flat-square)](https://github.com/a-lab-nagoya/xarray-cube/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nxarray extension for spectral cube analysis\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-lab-nagoya/xarray-cube/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
