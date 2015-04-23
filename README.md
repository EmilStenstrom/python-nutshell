# python-nutshell
A minimal python library to access Nutshell CRM:s JSON-RPC API.

## Installation

```python
pip install nutshell
```

## Example of usage
First create a [Nutshell **APIKEY**](http://www.import2.com/questions/235-how-do-i-get-nutshell-crm-api-key). Then Use the e-mail adress one of your existing users as the **USERNAME**.

```python
from nutshell import NutshellAPI

USERNAME = "example@example.com"
APIKEY = "000000000000000000000000000000000000000000000"

api = NutshellAPI(USERNAME, APIKEY)
accounts = api.findAccounts()
for account in accounts:
    print "-" * 80
    print "Account:"
    for field, value in account.items():
        print "%30s: %s" % (field, value)
```

The api object converts all method calls on it to JSON-RPC calls against [Nutshell's API](https://www.nutshell.com/api/). The [API documentation has a list possible calls](https://www.nutshell.com/api/detail/class_core.html), including parameters.
