# Brena
Nerdy CLI invoice generator. Brena generates invoices based on a .toml file you define.
You can do everything in the terminal. No need to open your browser and trouble yourself. Add a few lines, then you are done.

To install it type:
```bash
pip install brena
```

Then you need to create a `brena.toml` file somewhere, with the following contents that will define what invoices get generated.
Example of such a file and a description can be found below. How to use it?


## Usage
If you installed brena and defined your `brena.toml` file, then you can just.
```bash
brena
```
To generate all the invoices or
```bash
brena invoicecode1 invoicecode2
```
To generate only invoices with specific codes.

You can read a bit more after typing
```bash
brena --help
```

## Config: brena.toml
Below you can see an example of the required `brena.toml` file.
Brena expects this file to be found in current working directory.

``` toml
[companies.default]  # important to keep it as default 
  name = "Name Of Your Company"
  address_line_1 = "Some streeet 8/10"
  address_line_2 = "11-111 Some City"
  nip = "Your tax id number here if any"
  language = "pl"
  bank_accounts = { PLN = "PL11 1111 1111 1111 1111", EUR = "PL11 1111 1111 1111 1111" }

[companies.someclient]
  name = "Some Client Sp. z o. o."
  address_line_1 = "Another street"
  address_line_2 = "01-111 Warsaw"
  nip = "Your clients tax id if any"


[[invoices]]
  code = "01/12/2020"
  company = "someclient"
  currency = "PLN" # this value needs to be found in bank_accounts keys
  language = "pl"  # for now we only support pl and en
  dates = { issued = "2020-12-25", sold = "2020-12-31", due_to = "2021-01-15"}

  [[invoices.positions]]
    name = "IT service"
    quantity = 1
    amount = 15000
    vat_stake = 23


[[invoices]]
  code = "02/12/2020"
  company = "someclient"
  currency = "EUR"
  language = "en"
  dates = { issued = "2020-12-25", sold = "2020-12-31", due_to = "2021-01-10"}

  [[invoices.positions]] 
    name = "IT services"
    quantity = 172.5
    amount = 85.2
    vat_stake = 23
  
  [[invoices.positions]] 
    name = "Additional invoice position"
    quantity = 1
    amount = 82
    vat_stake = 23
```

## Dependencies

jinja2
toml 
WeasyPrint 
typer

## Docker 
TODO