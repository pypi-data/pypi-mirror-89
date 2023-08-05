# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spymock']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-spymock',
    'version': '0.1.0',
    'description': '',
    'long_description': '# spymock\n\nThis library provides `SpyMock` which is similar to [`MagicMock`](https://docs.python.org/3/library/unittest.mock.html#magic-mock) but recording function return values and exceptions on `call_values_or_exceptions` attribute.\n\n## Installation\n\n```\npip install spymock\n```\n\n## Usage\n\nUse `spymock.spy` function as-like [`patch.object`](https://docs.python.org/3/library/unittest.mock.html#patch-object) to spy and mock the target attribute like:\n\n```python\nimport urllib.request\n\nfrom spymock import spy\n\n\ndef request():\n    url = "http://httpbin.org/json"\n    req = urllib.request.Request(url)\n    with urllib.request.urlopen(req) as res:\n        return json.loads(res.read())\n\n\ndef test_request_with_spy():\n    with spy(urllib.request, "urlopen") as s:\n        assert request() == {\n            "slideshow": {\n                "author": "Yours Truly",\n                "date": "date of publication",\n                "slides": [\n                    {"title": "Wake up to WonderWidgets!", "type": "all"},\n                    {\n                        "items": [\n                            "Why <em>WonderWidgets</em> are great",\n                            "Who <em>buys</em> WonderWidgets",\n                        ],\n                        "title": "Overview",\n                        "type": "all",\n                    },\n                ],\n                "title": "Sample Slide Show",\n            }\n        }\n\n        # \'s\' is like MagicMock but it has \'call_values_or_exceptions\' attribute\n        assert len(s.call_values_or_exceptions) == 1\n\n        r = s.call_values_or_exceptions[0]\n        assert isinstance(r, HTTPResponse)\n        assert r.status == 200\n        assert r.reason == "OK"\n```\n\nOr directly create `spymock.SpyMock` instance as-like [`MagicMock`](https://docs.python.org/3/library/unittest.mock.html#magic-mock) like:\n\n```python\nimport urllib.request\n\nfrom spymock import SpyMock\n\n\ndef request():\n    url = "http://httpbin.org/json"\n    req = urllib.request.Request(url)\n    with urllib.request.urlopen(req) as res:\n        return json.loads(res.read())\n\n\ndef test_request_with_spymock():\n    s = SpyMock(request)\n    assert s() == {\n        "slideshow": {\n            "author": "Yours Truly",\n            "date": "date of publication",\n            "slides": [\n                {"title": "Wake up to WonderWidgets!", "type": "all"},\n                {\n                    "items": [\n                        "Why <em>WonderWidgets</em> are great",\n                        "Who <em>buys</em> WonderWidgets",\n                    ],\n                    "title": "Overview",\n                    "type": "all",\n                },\n            ],\n            "title": "Sample Slide Show",\n        }\n    }\n\n    # \'s\' is like MagicMock but it has \'call_values_or_exceptions\' attribute\n    assert len(s.call_values_or_exceptions) == 1\n\n    r = s.call_values_or_exceptions[0]\n    assert r == {\n        "slideshow": {\n            "author": "Yours Truly",\n            "date": "date of publication",\n            "slides": [\n                {"title": "Wake up to WonderWidgets!", "type": "all"},\n                {\n                    "items": [\n                        "Why <em>WonderWidgets</em> are great",\n                        "Who <em>buys</em> WonderWidgets",\n                    ],\n                    "title": "Overview",\n                    "type": "all",\n                },\n            ],\n            "title": "Sample Slide Show",\n        }\n    }\n```\n\n## License\n\nDistributed under the terms of the [MIT license](./LICENSE).\n',
    'author': 'lambdalisue',
    'author_email': 'lambdalisue@hashnote.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fixpoint/python-spymock',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
