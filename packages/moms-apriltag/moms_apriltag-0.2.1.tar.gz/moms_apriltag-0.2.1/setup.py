# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moms_apriltag', 'moms_apriltag.tags']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'moms-apriltag',
    'version': '0.2.1',
    'description': 'Generate apriltags',
    'long_description': '![](https://github.com/MomsFriendlyRobotCompany/moms_apriltag/blob/master/example/apriltag_target.png?raw=true)\n\n# Apriltag Camera Calibration Board Generator\n![CheckPackage](https://github.com/MomsFriendlyRobotCompany/moms_apriltag/workflows/CheckPackage/badge.svg)\n![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/moms_apriltag)\n[![Latest Version](https://img.shields.io/pypi/v/moms_apriltag.svg)](https://pypi.python.org/pypi/moms_apriltag/)\n[![image](https://img.shields.io/pypi/pyversions/moms_apriltag.svg)](https://pypi.python.org/pypi/moms_apriltag)\n[![image](https://img.shields.io/pypi/format/moms_apriltag.svg)](https://pypi.python.org/pypi/moms_apriltag)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/moms_apriltag?color=aqua)\n\nWhy? There didn\'t really seem to be an easy way to do this IMHO.\n\n## Install\n\n```\npip install moms_apriltag\n```\n\n## Usage\n\nThis package create a simple numpy image that can then be saved\nto a PNG or JPEG image and printed.\n\nSupported families: `tag16h5`, `tag25h9`, `tag36h10`, `tag36h11`\n\n```\n#!/usr/bin/env python3\nimport moms_apriltag as apt\nimport numpy as np\nimport imageio\n\n\nif __name__ == \'__main__\':\n    family = "tag36h10"\n    shape = (6,8)\n    filename = "apriltag_target.png"\n    size = 50\n\n    tgt = apt.board(shape, family, size)\n    imageio.imwrite(filename, tgt)\n```\n\n# MIT License\n\n**Copyright (c) 2020 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/apriltag_gen/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
