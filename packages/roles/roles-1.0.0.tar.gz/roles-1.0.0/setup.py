# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roles']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'roles',
    'version': '1.0.0',
    'description': 'Role based software development',
    'long_description': '# Roles\n\nLibrary for Role based development.\n\nPythonic implementation of the DCI (Data Context Interaction) pattern\n(http://www.artima.com/articles/dci_vision.html).\n\nThe big difference with mixins is that this role is applied only to the subject\ninstance, not to the subject class (alas, a new class is constructed).\n\nRoles can be assigned and revoked. Multiple roles can be applied to an\ninstance. Revocation can happen in any particular order.\n\nHomepage: http://github.com/amolenaar/roles\n\nReleases: http://pypi.python.org/pypi/roles\n\n\n## Using Roles\n\nAs a basic example, consider a domain class:\n\n```python\n>>> class Person:\n...     def __init__(self, name):\n...         self.name = name\n>>> person = Person("John")\n```\n\nThe instance should participate in a collaboration in which it fulfills a\nparticular role:\n\n```python\n>>> from roles import RoleType\n>>> class Carpenter(metaclass=RoleType):\n...     def chop(self):\n...          return "chop, chop"\n\n```\nAssign the role to the person:\n\n```python\n>>> Carpenter(person)\t\t\t\t# doctest: +ELLIPSIS\n<__main__.Person+Carpenter object at 0x...>\n>>> person\t\t\t\t\t# doctest: +ELLIPSIS\n<__main__.Person+Carpenter object at 0x...>\n\n```\n\nThe person is still a Person:\n\n```python\n>>> isinstance(person, Person)\nTrue\n\n```\n... and can do carpenter things:\n\n```python\n>>> person.chop()\n\'chop, chop\'\n\n```\n\nSee [`roles.py`](http://github.com/amolenaar/roles/blob/master/roles.py) for more examples.\n\n## Context\n\nRoles make a lot of sense when used in a context. A classic example is the\nmoney transfer example. Here two accounts are used and an amount of money is\ntransfered from one account to the other. So, one account playes the role of\nsource account and the other plays the role of target account.\n\nAn example can be found in [`example.py`](http://github.com/amolenaar/roles/blob/master/example.py).\n',
    'author': 'Arjan Molenaar',
    'author_email': 'gaphor@gmail.com',
    'maintainer': 'Arjan Molenaar',
    'maintainer_email': 'gaphor@gmail.com',
    'url': 'https://github.com/amolenaar/roles',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
