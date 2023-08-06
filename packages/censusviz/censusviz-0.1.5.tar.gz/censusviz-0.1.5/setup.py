# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['censusviz']

package_data = \
{'': ['*']}

install_requires = \
['descartes', 'geopandas', 'lxml', 'matplotlib', 'pandas', 'requests']

setup_kwargs = {
    'name': 'censusviz',
    'version': '0.1.5',
    'description': 'A Python package to make it easier to visualize Census data.',
    'long_description': '# censusviz \n\n![](https://github.com/elliotttrio/censusviz/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/elliotttrio/censusviz/branch/main/graph/badge.svg)](https://codecov.io/gh/elliotttrio/censusviz) ![Release](https://github.com/elliotttrio/censusviz/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/censusviz/badge/?version=latest)](https://censusviz.readthedocs.io/en/latest/?badge=latest)\n\nThis package helps users more easily visualize maps using Census Population Estimate API and the Census Cartographic GeoJSON boundary files. It transforms GeoJSON files into easy to work with GeoPandas.GeoDataFrame and plot choropleth maps.\n\n## Installation\n\n```bash\npip install censusviz\n```\n## Dependencies\n\n- python = "^3.6"\n- pandas \n- pyproj \n- requests \n- numpy \n- shapely \n- gdal = [Wheels for Windows User](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)\n- fiona = [Wheels for Windows User](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)\n- geopandas \n- matplotlib \n- descartes \n- lxml\n\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://censusviz.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/elliotttrio/censusviz/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Elliott',
    'author_email': 'eat2153@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/elliotttrio/censusviz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
