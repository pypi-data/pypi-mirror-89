# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chanim']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.1.1,<0.2.0']

entry_points = \
{'manim.plugins': ['chanim = chanim']}

setup_kwargs = {
    'name': 'chanim',
    'version': '0.0.1',
    'description': 'Addon for manim which makes drawing chemical figures easier.',
    'long_description': '# Chanim\nThis is an extension to 3BlueBrown\'s [Manim](https://www.github.com/ManimCommunity/manim) library,\nfor making videos regarding chemistry.\n\n## Installation\n1. Get manim as described [here](https://manimce.readthedocs.io/en/latest/installation.html) according to your OS,  or `pip install manimce` (will be `pip install manim` [soon](https://github.com/pypa/pypi-support/issues/450)). You\'ll have to download other required modules as explained at the manim page.\n2. Clone the contents of this repository.\n3. Open a terminal in the cloned directory and run `pip install -e .` (note: requires `pip` to be installed, see how to install for your OS)\n\nThat\'s about it. You can now do `from chanim import <*|object_name>` like any regular Python package. \n\n## Usage\n```py\nfrom chanim import *\n\nclass MoleculeOrReaction(Scene):\n    <name> = ChemObject(<chemfig code>)\n    self.play(Write(<name>))\n```\n\nType this into a python (`.py`) file (changing whatever\'s necessary, i.e. stuff inside the angle brackets). I\'ll assume you named it `chem.py`\n\nIn your command prompt/terminal write this (assuming you\'re in your project directory):\n\n```sh\nmanim chem.py MoleculeOrReaction -pl\n```\nThis\'ll render your Scene and preview it in your default player (in \'l\'ow quality).\n\nHere\'s a little example of it working.\n\n```py\nfrom chanim import *\n\nclass ChanimScene(Scene):\n    def construct(self):\n        chem = ChemWithName("*6((=O)-N(-CH_3)-*5(-N=-N(-CH_3)-=)--(=O)-N(-H_3C)-)")\n\n        self.play(chem.creation_anim())\n        self.wait()\n```\n![output](https://github.com/raghavg123/chanim/blob/ManimCE-TexTemplate-Working/ChanimScene.gif)\nCongrats! You\'ve written and played your first animation (or "chanimation" should I say)\n\nExplore the code and docs (not written yet) for more on how to use chanim.\n\n## Abilities\nCurrently chanim only supports drawing compounds and reactions along with a few chemfig commands (such as coordinate bonds and complexes etc.) but more is to come! If you have a suggestion, file an issue with a proper tag.\n\n## A Quick Note\nThere may be some faulty code and a lot of this may not be well made/documented. Feel free to file an issue if something doesn\'t work properly.\n\n~~Also, at the moment chanim won\'t work with the [community version of manim](https://github.com/ManimCommunity/manim) due to the changes in how the TeX templates are used and modified, which I haven\'t really figured out how to incorporate with chanim. It may become an addon at some point, but not anytime in the near future unfortunately. Thus consider using the 3b1b/manim version instead.~~\n\n**Chanim is compatible with ManimCE now, but unforunately it is not backward compatible with the 3b1b version.** Also, it isn\'t an "addon" for the time being, so you\'ll still have to clone it and use it like earlier.\n',
    'author': 'kilacoda',
    'author_email': 'kilacoda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/raghavg123/chanim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
