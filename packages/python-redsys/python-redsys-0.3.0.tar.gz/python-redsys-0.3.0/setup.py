# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redsys']

package_data = \
{'': ['*']}

install_requires = \
['pycrypto>=2.6.1,<3.0.0']

setup_kwargs = {
    'name': 'python-redsys',
    'version': '0.3.0',
    'description': 'A simple, clean and less dependant client to handle payments through Redsys.',
    'long_description': '# Welcome to python-redsys!\n\nA simple, clean and less dependant client to handle payments through the\nRedsys platform using one of the available methods: _redirect connection_ or (secure method).\n\nThe purpose of this library is to provide a normalized interface between\nRedsys and other Python applications.\n\n**About RedirectClient**\n\nAlthough _redirect connection_ depends on a webserver to resolve the\ncommunication step, the RedirectClient provided in this library does not\nassume any kind of procedure to resolve that step; it merely prepares\nthe necessary parameters to make a request and handles the corresponding\nresponse parameters. That\'s what less dependant means.\n\n## Example using _redirect connection_\n\n### 1. Instantiate the redirect client\n\n```{.sourceCode .python}\nfrom decimal import Decimal as D, ROUND_HALF_UP\nfrom redsys import currencies, languages, parameters, transactions\nfrom redsys.client import RedirectClient\n\nsecret_key = "123456789abcdef"\nsandbox = False\nclient = RedirectClient(secret_key, sandbox)\n```\n\n### 2. Create a request\n\n```{.sourceCode .python}\nrequest = client.create_request()\n```\n\n### 3. Set up the request parameters\n\n```python\nrequest.merchant_code = "100000001"\nrequest.terminal = "1"\nrequest.transaction_type = transactions.STANDARD_PAYMENT\nrequest.currency = currencies.EUR\nrequest.order = "000000001"\n# The amount must be defined as decimal and pre-formatted with only two decimals\nrequest.amount = D("10.56489").quantize(D(".01"), ROUND_HALF_UP)\nrequest.merchant_data = "merchant data for tracking purpose like order_id, session_key, ..."\nrequest.merchant_name = "Example Commerce"\nrequest.titular = "Example Ltd."\nrequest.product_description = "Products of Example Commerce"\nrequest.merchant_url = "https://example.com/redsys/response"\n```\n\n### 4. Prepare the request\n\nThis method returns a dict with the necessary post parameters that are\nneeded during the communication step.\n\n```python\nargs = client.prepare_request(request)\n```\n\n### 5. Communication step\n\nRedirect the _user-agent_ to the corresponding RedSys\'s endpoint using\nthe post parameters given in the previous step.\n\nAfter the payment process is finish, RedSys will respond making a\nrequest to the `merchant_url` defined in step 3.\n\n### 6. Create and check the response\n\nCreate the response object using the received parameters from Redsys.\nThe method `create_response()` throws a `ValueError` in case the\nreceived signature is not equal to the calculated one using the\ngiven `merchant_parameters`. This normally means that the response **is\nnot coming from Redsys** or that it **has been compromised**.\n\n```python\nsignature = "YqFenHc2HpB273l8c995...."\nmerchant_parameters = "AndvIh66VZdkC5TG3nYL5j4XfCnFFbo3VkOu9TAeTs58fxddgc..."\nsignature_version = "HMAC_SHA256_V1"\nresponse = client.create_response(signature, merchant_parameters, signature_version)\nif response.is_paid():\n    # Do the corresponding actions after a successful payment\nelse:\n    # Do the corresponding actions after a failed payment\n    raise Exception(response.response, response.message)\n```\n\n**Methods for checking the response:**\n\nAccording to the RedSys documentation:\n\n- `response.is_paid()`: Returns `True` if the response code is\n  between 0 and 99 (both included).\n- `response.is_canceled()`: Returns `True` if the response code\n  is 400.\n- `response.is_refunded()`: Returns `True` if the response code\n  is 900.\n- `response.is_authorized()`: Returns `True` if the response is\n  **paid**, **refunded** or **canceled**.\n\nAlso, you can directly access the code or the message defined in Redsys\ndocumentation using `response.response_code` or\n`response.response_message`.\n\n## Contributions\n\nPlease, feel free to send any contribution that maintains the _less\ndependant_ philosophy.\n',
    'author': 'Andrés Reverón Molina',
    'author_email': 'andres@reveronmolina.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/systemallica/python-redsys',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
