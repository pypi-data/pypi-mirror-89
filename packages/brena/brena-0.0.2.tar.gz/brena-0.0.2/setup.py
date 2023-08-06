# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brena', 'brena.invoice_templates', 'brena.jinja']

package_data = \
{'': ['*']}

install_requires = \
['WeasyPrint>=52.1,<53.0',
 'jinja2>=2.11.1,<3.0.0',
 'toml>=0.10.0,<0.11.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['braindead = brena.cli:cli']}

setup_kwargs = {
    'name': 'brena',
    'version': '0.0.2',
    'description': 'Simple invoice generation.',
    'long_description': '# Brena\nNerdy CLI invoice generator. Brena generates invoices based on a .toml file you define.\nYou can do everything in the terminal. No need to open your browser and trouble yourself. Add a few lines and be done! \n\nWhy you might ask? Because I hate to leave the terminal - that\'s it!\n\n## Installation\nTo install it type:\n```bash\npip install brena\n```\nand you are done. Brena depends on [weasyprint](https://github.com/Kozea/WeasyPrint/), so you might be required to install additional requirements. Look at [weasyprint docs](https://weasyprint.readthedocs.io/en/stable/).\nIf you don\'t want to do that - check out the docker option.\n\n## Usage\nIf you have defined your `brena.toml` file (how to do it is shown below), then you can just:\n```bash\nbrena\n```\nTo generate all the invoices or\n```bash\nbrena invoicecode1 invoicecode2\n```\nTo generate only invoices with specific codes.\n\nYou can read a bit more about available commands after typing\n```bash\nbrena --help\n```\n\n## Config: brena.toml\nBelow you can see an example of the required `brena.toml` file.\nBrena expects this file to be found in current working directory.\n\n``` toml\n[companies.default]  # important to keep it as default \n  name = "Name Of Your Company"\n  address_line_1 = "Some streeet 8/10"\n  address_line_2 = "11-111 Some City"\n  nip = "Your tax id number here if any"\n  language = "pl"\n  bank_accounts = { PLN = "PL11 1111 1111 1111 1111", EUR = "PL11 1111 1111 1111 1111" }\n\n[companies.someclient]\n  name = "Some Client Sp. z o. o."\n  address_line_1 = "Another street"\n  address_line_2 = "01-111 Warsaw"\n  nip = "Your clients tax id if any"\n\n\n[[invoices]]\n  code = "01/12/2020"\n  company = "someclient"\n  currency = "PLN" # this value needs to be found in bank_accounts keys\n  language = "pl"  # for now we only support pl and en\n  dates = { issued = "2020-12-25", sold = "2020-12-31", due_to = "2021-01-15"}\n\n  [[invoices.positions]]\n    name = "IT service"\n    quantity = 1\n    amount = 15000\n    vat_stake = 23\n\n\n[[invoices]]\n  code = "02/12/2020"\n  company = "someclient"\n  currency = "EUR"\n  language = "en"\n  dates = { issued = "2020-12-25", sold = "2020-12-31", due_to = "2021-01-10"}\n\n  [[invoices.positions]] \n    name = "IT services"\n    quantity = 172.5\n    amount = 85.2\n    vat_stake = 23\n  \n  [[invoices.positions]] \n    name = "Additional invoice position"\n    quantity = 1\n    amount = 82\n    vat_stake = 23\n```\nFor now I only support toml, maybe yaml in the future. Why toml over yaml? No reason, just my preference in this case.\n\n## Dependencies\n\n[jinja2]()\ntoml \nWeasyPrint \ntyper\n\n# Technology\nThis bases on\n[toml](https://github.com/uiri/toml), [weasyprint](https://github.com/Kozea/WeasyPrint/) and [jinja2](https://github.com/pallets/jinja).\n\nToml is used for configuration.\nweasyprint gets the html template rendered to pdf.\nLastly jinja2 to add some contexts here and there.\n\nFormatting of the code is done using [black](https://github.com/psf/black), [isort](https://github.com/timothycrosley/isort).\n[flake8](https://gitlab.com/pycqa/flake8), [autoflake](https://github.com/myint/autoflake) and [bandit](https://github.com/PyCQA/bandit/) to check for potential vulns.\n\nVersioning is done with [bumpversion](https://github.com/peritus/bumpversion).\nPatch for merges to develop, minor for merged to master. Merge to master means release to pypi.\n\nAnd wonderful [poetry](https://github.com/python-poetry/poetry) as dependency manager.\n\nCLI is done with [typer](https://github.com/tiangolo/typer) <- wonderful CLI library.\n\nI use type hinting where it\'s possible.\n\nTo start developing you need to install poetry\n`pip install poetry` and then just `poetry install`. \n\n## Docker \nTODO\n\n## Known make commands\n```bash\nflake\nisort\nisort-inplace\nbandit\nblack\nlinters\nbumpversion\nblack-inplace\nautoflake-inplace\nformat-inplace\n```\nMost important ones are `make linters` and `make format-inplace`. Before each commit it\'s required to run these checks.\n\n## License\nMIT\n\n',
    'author': 'Olaf Górski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://grski.pl/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
