# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiounu']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'mo-dots>=4.2.20340,<5.0.0',
 'pytest-aiohttp>=0.3.0',
 'pytest-asyncio>=0.14.0',
 'pytest>=6.1.1']

setup_kwargs = {
    'name': 'aiounu',
    'version': '0.1.2',
    'description': 'Asyncio module for unu in Python3 using aiohttp.',
    'long_description': '\n# aiounu\n\nAn asyncio module for [unu](https://u.nu/) in Python3 using aiohttp. Forked from\n[vcinex/unu](https://github.com/vcinex/unu).\n\n## Install\n\n```sh\npip install aiounu\n```\n\n## Use\n\n```python\nimport aiounu as unu\n\ntest_url = "https://example.com/?test=52e838e8-0943-4ccb-bfd8-ae6bb3173bd2"\nunu_resp = await unu.shorten(url=test_url, output_format="dot", keyword="")\nprint(unu_resp.shorturl)\n```\n\n## Example Result\n\nIf `output_format` is set to **dot** (The default), the resulting JSON object properties will be accessible (Thanks to\n[mo-dots](https://pypi.org/project/mo-dots/)) by both dot.notation and dict[\'notation\'].\n\n```json\n{\n  "url": {\n    "keyword": "kfuns",\n    "url": "https://example.com/?test=52e838e8-0943-4ccb-bfd8-ae6bb3173bd2",\n    "title": "Example Domain",\n    "date": "2020-12-22 08:44:33",\n    "ip": "22.42.219.59"\n  },\n  "status": "error",\n  "message": "https://example.com/?test=52e838e8-0943-4ccb-bfd8-ae6bb[...] added to database<br/>(Could not check Google Safe Browsing: Bad Request)",\n  "title": "Example Domain",\n  "shorturl": "https://u.nu/kfuns",\n  "statusCode": 200\n}\n```\n\nOnly the `url` variable is necessary. For a runnable example, see\n[tests/test_shorten.py](https://github.com/TensorTom/aiounu/blob/master/tests/test_shorten.py) or clone the repo\nand run [pytest](https://docs.pytest.org/en/stable/).\n\n----------------------------------------\n\nMIT License',
    'author': 'TensorTom',
    'author_email': '14287229+TensorTom@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tensortom/aiounu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
