# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinderdata']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.4,<0.5',
 'matplotlib>=3.2,<4.0',
 'pandas>=1.0,<2.0',
 'seaborn>=0.10,<0.11',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tinderdata = tinderdata.__main__:app']}

setup_kwargs = {
    'name': 'tinderdata',
    'version': '0.4',
    'description': 'A silly utility to explore your Tinder data.',
    'long_description': '<h1 align="center">\n  <b>tinderdata</b>\n</h1>\n\nA very simple package to get insight on your Tinder usage.\n\n## Install\n\nThis code is compatible with `Python 3.6+`.\nIf for some reason you have a need for it, you can simply install it in your virtual enrivonment with:\n```bash\npip install tinderdata\n```\n\n## Usage\n\nThis utility requires that you export your data from the Tinder platform, as described [here](https://www.help.tinder.com/hc/en-us/articles/115005626726-How-do-I-request-a-copy-of-my-personal-data-).\nYou should obtain a single `tinderdata.json` file, which is the input required for this script.\n\nWith this package installed in the activated enrivonment, it can be called through `python -m tinderdata` or through a newly created `tinderdata` command.\n\nDetailed usage goes as follows:\n```\nUsage: tinderdata [OPTIONS] [DATA_PATH]\n\n  Get insight on your Tinder usage.\n\nArguments:\n  [DATA_PATH]  Location, relative or absolute, of the exported JSON file with\n               your user data.\n\n\nOptions:\n  --show-figures / --no-show-figures\n                                  Whether or not to show figures when plotting\n                                  insights.  [default: False]\n\n  --save-figures / --no-save-figures\n                                  Whether or not to save figures when plotting\n                                  insights.  [default: False]\n\n  --log-level TEXT                The base console logging level. Can be\n                                  \'debug\', \'info\', \'warning\' and \'error\'.\n                                  [default: info]\n\n  --install-completion            Install completion for the current shell.\n  --show-completion               Show completion for the current shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n```\n\nAn example command is then:\n```\npython -m tinderdata path_to_tinderdata.json --save-figures --log-level debug\n```\n\nThe script print out a number of insight statements, and finally the text you should paste to get a Sankey diagram.\nIt will then create a `plots` folder and populate it with visuals.\n\nYou can otherwise import the high-level object from the package, and use at your convenience:\n```python\nfrom tinderdata import TinderData\n\ntinder = TinderData("path/to/tinderdata.json")\ntinder.output_sankey_string()\ntinder.plot_messages_loyalty(showfig=True, savefig=False)\n```\n\n## Output example\n\nHere are examples of the script\'s outputs:\n\n![Example_1](plots/messages_monthly_stats.png)\n\n![Example_2](plots/swipes_weekdays_stats.png)\n\n## License\n\nCopyright &copy; 2019-2020 Felix Soubelet. [MIT License][license]\n\n[license]: https://github.com/fsoubelet/Tinder_Data/blob/master/LICENSE\n',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/Tinder_Data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
