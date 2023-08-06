# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpx_linesman']

package_data = \
{'': ['*']}

install_requires = \
['geopy>=2.0.0,<3.0.0', 'gpxpy>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['linesman = gpx_linesman:run']}

setup_kwargs = {
    'name': 'gpx-linesman',
    'version': '0.1.2',
    'description': 'Command line tool for measuring the straightness of a gpx track',
    'long_description': '# linesman\n\n`linesman` is a small python command line tool calculating quality measures for the\nstraightness of a gpx track. The project is inspired by the "I attempted to\ncross \\<country\\> in a completely straight line" series by the youtuber\n[GeoWizard](https://www.youtube.com/channel/UCW5OrUZ4SeUYkUg1XqcjFYA).\n\n## Installation\n\nAs a python package, `linesman` is installed via pip (the package is named\n`gpx-linesman`):\n\n```\npip install gpx-linesman\n```\n\nAfter installing the package, you should be able to run linesman:\n\n```\nlinesman --help\n```\n\n## Usage\n\nCurrently, three deviation measures are implemented: `max_m` (maximum deviation\nto the straight line in meters), `avg_m` (average deviation to the straight line\nin meters) and `avg_sq_m` (average squared deviation).\n\nWithout special arguments, the maximum deviation is being calculated:\n\n```\nlinesman <file.gpx> <lon_start,lat_start> <lon_end,lat_end>\n```\n\nCalculating the average deviation:\n\n```\nlinesman <file.gpx> <lon_start,lat_start> <lon_end,lat_end> --using avg_m\n```\n\nFor an example gpx file, see [`examples/simple.gpx`](examples/simple.gpx).\n\n',
    'author': 'burrscurr',
    'author_email': 'burrscurr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
