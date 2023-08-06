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
    'version': '0.0.1',
    'description': 'Simple invoice generation.',
    'long_description': '# Brena\nNerdy CLI invoice generator. Brena generates invoices based on a .toml file you define.\nYou can do everything in the terminal. No need to open your browser and trouble yourself. Add a few lines, then you are done.\n\nTo install it type:\n```bash\npip install brena\n```\n\nThen you need to create a `brena.toml` file somewhere, with the following contents that will define what invoices get generated.\nExample of such a file and a description can be found below. How to use it?\n\n\n## Usage\nIf you installed brena and defined your `brena.toml` file, then you can just.\n```bash\nbrena\n```\nTo generate all the invoices or\n```bash\nbrena invoicecode1 invoicecode2\n```\nTo generate only invoices with specific codes.\n\nYou can read a bit more after typing\n```bash\nbrena --help\n```\n\n## Config: brena.toml\nBelow you can see an example of the required `brena.toml` file.\nBrena expects this file to be found in current working directory.\n\n``` toml\n[companies.default]  # important to keep it as default \n  name = "Name Of Your Company"\n  address_line_1 = "Some streeet 8/10"\n  address_line_2 = "11-111 Some City"\n  nip = "Your tax id number here if any"\n  language = "pl"\n  bank_accounts = { PLN = "PL11 1111 1111 1111 1111", EUR = "PL11 1111 1111 1111 1111" }\n\n[companies.someclient]\n  name = "Some Client Sp. z o. o."\n  address_line_1 = "Another street"\n  address_line_2 = "01-111 Warsaw"\n  nip = "Your clients tax id if any"\n\n\n[[invoices]]\n  code = "01/12/2020"\n  company = "someclient"\n  currency = "PLN" # this value needs to be found in bank_accounts keys\n  language = "pl"  # for now we only support pl and en\n  dates = { issued = "2020-12-25", sold = "2020-12-31", due_to = "2021-01-15"}\n\n  [[invoices.positions]]\n    name = "IT service"\n    quantity = 1\n    amount = 15000\n    vat_stake = 23\n\n\n[[invoices]]\n  code = "02/12/2020"\n  company = "someclient"\n  currency = "EUR"\n  language = "en"\n  dates = { issued = "2020-12-25", sold = "2020-12-31", due_to = "2021-01-10"}\n\n  [[invoices.positions]] \n    name = "IT services"\n    quantity = 172.5\n    amount = 85.2\n    vat_stake = 23\n  \n  [[invoices.positions]] \n    name = "Additional invoice position"\n    quantity = 1\n    amount = 82\n    vat_stake = 23\n```\n\n## Dependencies\n\njinja2\ntoml \nWeasyPrint \ntyper\n\n## Docker \nTODO',
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
