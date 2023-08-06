# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simple_hierarchy']

package_data = \
{'': ['*'], 'simple_hierarchy': ['examples/*']}

install_requires = \
['numpy==1.19.3']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.3.0,<4.0.0'],
 ':python_version >= "3.7" and python_version < "4.0"': ['torch>=1.7.1,<2.0.0']}

setup_kwargs = {
    'name': 'simple-hierarchy',
    'version': '1.0.1',
    'description': 'Simple hierarchal models in PyTorch.',
    'long_description': "[![Tests](https://github.com/rajivsarvepalli/SimpleHierarchy/workflows/Tests/badge.svg)](https://github.com/rajivsarvepalli/SimpleHierarchy/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/rajivsarvepalli/SimpleHierarchy/branch/master/graph/badge.svg)](https://codecov.io/gh/rajivsarvepalli/SimpleHierarchy)\n[![PyPI](https://img.shields.io/pypi/v/simple-hierarchy.svg)](https://pypi.org/project/simple-hierarchy/)\n[![Documentation Status](https://readthedocs.org/projects/simplehierarchy/badge/?version=latest)](https://simplehierarchy.readthedocs.io/en/latest/?badge=latest)\n\n# Hierarchical Classification Networks\nWhen looking at the task for classifying something where hierarchies were intrinsic to the classes, I searched for any libraries that might do very simple classification using grouped classes with hierarchies. However, I did not find any libraries that were suited for this relatively simple task. So I sought to create a more general solution that others can hopefully benefit from.\n\n\nThe concept is quite simple: create general architecture for groupings of classes dependent on each other. So starting with a basic concept of model, I looked to make something in PyTorch that represented my idea.\n\n# Example Use Case\nLet us take an image geolocation problem where we want the location for city, county, and district. We will call these groupings a,b,c respectively. Given an image input, we want to predict all 3 classes but also need an architecture in which these relationships are properly represented. The network architecture below illustrates a possible solution (that this package will attempt to implement with a degree of adaptability).\nThe architecture can be visualized as so with an input image:\n![Network Architecture](https://raw.githubusercontent.com/rajivsarvepalli/SimpleHierarchy/master/images/network.svg)\n\n where the class hierarchy is like so\n\n![Class Heirarchy](https://raw.githubusercontent.com/rajivsarvepalli/SimpleHierarchy/master/images/tree.svg)\n\nThe class hierarchy is a similar structure to an example within this package. Each node has a tuple of a named grouping and the number of classes within that grouping. This the reason for the sizes in the final outputs in the network architecture. The large green plus signs within circles are used to indicate concatenation of the two input (green arrowed lines) leading into them. This is why the sections for class b and c have input size 4096 + 1024 = 5120.\n# Installation\nThe required version of Python for this package is >= 3.7.\n\nTo install this package, first, install PyTorch. You can use `requirements.txt` to install PyTorch 1.7, however, the best way to install is to go to [PyTorch's website](https://pytorch.org/get-started/locally/) and follow the instructions there. This package may work with versions less than 1.7, but it was only tested on PyTorch 1.7. This package will allow for versions of PyTorch >= 1.0, but please know only 1.7 is tested.\nUsing pip makes this installation easy and simple once PyTorch is installed. This can be installed through\n```\npip install simple-hierarchy-pytorch\n```\nThe repository can also be cloned and then built from source using poetry.\n\nFinally, this repository can simply be downloaded and imported as python code since there are essentially only two required classes here.\n# Getting Started\nThis architecture allows for simple yet adaptable hierarchal classifications for basic tasks that involve finite hierarchies. The package was targeted towards image classifications where there are multiple groups to classify something as but may serve other purposes equally well. Below is an example of how to use the package along with the defined class:\n```\nfrom simple_hierarchy.hierarchal_model import HierarchalModel\nhierarchy = {\n    ('A', 2) : [('B', 5)],\n    ('B', 5) : [('C', 7)]\n}\nmodel_base = nn.Sequential(\n  nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5),\n  nn.ReLU(),\n  nn.MaxPool2d(kernel_size=2, stride=2),\n  nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5),\n  nn.ReLU(),\n  nn.MaxPool2d(kernel_size=2, stride=2),\n  nn.Flatten(start_dim=1),\n  nn.Linear(in_features=1296, out_features=120),\n  nn.ReLU(),\n  nn.Linear(in_features=120, out_features=84),\n  nn.ReLU()\n)\nmodel = HierarchalModel(hierarchy, (84, 32, 32),base_model=model_base)\n# Example input\na = torch.rand(3,50,50).unsqueeze(0)\nmodel(a)\n```\nThen the model can be trained on an image dataset like any other model.\n\nAdditionally, there is [Jupyter notebook](https://github.com/rajivsarvepalli/SimpleHierarchy/blob/master/src/simple_hierarchy/examples/sample.ipynb) within this [repository](https://github.com/rajivsarvepalli/SimpleHierarchy) illustrates some examples of how to use and run these classes. Most of the Jupyter notebook is self-contained so all the necessary code is already inside there independent of the package. At the beginning is an example with this package as well.\nThe formulation is quite simple, so it should not be too much additional work to incorporate the HierarchalModel into your networks.\nHowever, the solution given here is quite simple and therefore can be implemented easily for specific cases. The HierarchalModel class just provides a general solution for more use cases and gave me chance to test and build some architectural ideas.\n## Authors\n\n* **Rajiv Sarvepalli** - *Created* - [rajivsarvepalli](https://github.com/rajivsarvepalli)\n",
    'author': 'Rajiv Sarvepalli',
    'author_email': 'rajiv@Sarvepalli.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rajivsarvepalli/SimpleHierarchy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
