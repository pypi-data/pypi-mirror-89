# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drizm_commons', 'drizm_commons.google', 'drizm_commons.sqla']

package_data = \
{'': ['*']}

extras_require = \
{'google': ['google-auth==1.23.0',
            'requests>=2.25.0,<3.0.0',
            'google-cloud-storage==1.35.0'],
 'sqla': ['sqlalchemy==1.3.20']}

setup_kwargs = {
    'name': 'drizm-commons',
    'version': '0.4.2',
    'description': 'Python3 commons for the Drizm organization',
    'long_description': '# Drizm Python Commons\n[![PyPI version](https://badge.fury.io/py/drizm-commons.svg)](https://badge.fury.io/py/drizm-commons)  \n\nThis package contains shared code used by\nthe Drizm organizations development team.  \n\nIt is not intended for public usage,\nbut you may still download,\nredistribute or modify it to your liking.\n\n## Requirements\n\nPython 3.8 supported.\n\n## Installation\n\nBasic Install (utils only):  \n``pip install drizm-commons``\n\nInstall SQLAlchemy features:  \n``pip install drizm-commons[sqla]``  \nInstall Google-Cloud utils:  \n``pip install drizm-commons[google]``  \nInstall everything:  \n``pip install drizm-commons[sqla,google]``\n\nImport as:  \n*import drizm_commons*\n\n## Features\n\n- GCP Utilities\n- Testing Utilities\n- Extras for working with Terraform\n- Basic Introspector for various\nSQLAlchemy classes\n\n## Google Cloud Tools\n\n**import drizm_commons.google**\n\n### force_obtain_id_token()\n\nCan be used to obtain an OIDC-Token for authenticating\nagainst GoogleCloud services.\n\n````python\nfrom drizm_commons.google import force_obtain_id_token\nfrom google.oauth2 import service_account\n\n\nauth = service_account.IDTokenCredentials.from_service_account_file(\n    "/path/to/svc.json",\n    target_audience="https://example.com/"\n)\ntoken = force_obtain_id_token(auth)\n# Returns an access token with the structure \'ey....\'\n````\n\n### TestStorageBucket\n\nUsed to generate a V4 Signed-URL for use with GCS.  \nThis can also be done using the GoogleCloudStorage\n\n````python\nfrom drizm_commons.google import TestStorageBucket\nfrom google.oauth2 import service_account\n\ncredentials = service_account.Credentials.from_service_account_file(\n    "path/to/svc.json"\n)\ntest_bucket = TestStorageBucket(\n    project_id="your-project-id",\n    credentials=credentials\n)\ntest_bucket.create()\n\n# ... do whatever you need to test ...\n\ntest_bucket.destroy()\n````\n\n## Utilities\n\n**Convinience Functions:**  \n````python\nfrom drizm_commons.utils import *\n\n\n# Check whether function name is dunder\nis_dunder("__name__")  # True\n\n# Check if a given string is a valid UUIDv4\nuuid4_is_valid("myvalue")  # False\n\n# Check if a URL is valid and the contents URL-Safe\nurl_is_http("https://myapp.com/")  # True\n\n# Get the current applications root path\nPath(get_application_root())\n````\n\n**Path with extra features:**\n````python\nfrom drizm_commons.utils import Path\n\n# Recursively delete a folder\npath = Path(__file__).parent\npath.rmdir(recursive=True)\n````\n\n**Cache last passed parameter:**\n````python\nfrom drizm_commons.utils import memoize\n\n\n@memoize\ndef foo(a):\n    return a\n\n\nfoo(3)  # 3\nfoo()  # 3\n````\n\n## SQLA Introspection\n\n````python\nfrom drizm_commons.inspect import SQLAIntrospector\n\n\ntable = SQLAIntrospector(my_table_instance)\n\n""" Attributes """\ntable.tablename  # get the name of the table\ntable.classname  # get the classname of the declarative instance\ntable.columns  # get all SQLA fields of the class\ntable.column_attrs  # get all SQLA fields + property and hybrid_property of the class\n````\n\n## Changelog\n\n### 0.1.1\n\n- Added SQLAlchemy JSON Encoder\n- Fixed bugs related to the Introspection\nAPI\n- Added table registry\n- Added additional utilities\n\n### 0.1.2\n\n- Added get_root_path and recursive delete\nPath utilities\n- Fixed various bugs\n\n### 0.2.0\n\n- Added full test suite\n- Added testing tools\n- Revamped introspection API\n- Provided additional overrides for the\nSQL connection adapter\n\n### 0.2.1\n\n- Added support for datetime JSON\nencoding\n\n### 0.2.2\n\n- Improved in-code documentation\n- Integrated additional utils from\ndrizm-django-commons\n\n### 0.3.0\n\n- Added introspection capabilities \nfor property and SQLAlchemy\'s\nhybrid_property\n- SQLAEncoder now respects property\nand hybrid_property on SQLA declarative\ninstances\n- Additional customizability hooks\nfor custom fields or data handling\n- Support for JSON-Encoding table\ninstances\n- Added SQLA as optional dependency\n- Added additional testing utilities\n\n### 0.3.1\n\n- Improved code documentation\n- Added docs\n- Added memoize function decorator\nto cache last previously passed\nfunction parameter\n\n### 0.3.2\n\n- Fixed issue with introspection API\npicking up validation methods\n\n### 0.3.3\n\n- Added additional tests and bugfixes\n\n### 0.3.4\n\n- Added support for comments and\nspecial character parsing to Tfvars\n\n### 0.4.0\n\n- Added method to force obtain\nGoogleCloudPlatform Id-Tokens\n\n### 0.4.1\n\n- Added function to convert\nCamelCase to snake_case\n\n### 0.4.2\n\n- Added TestStorageBucket\n- Updated docs\n- Added camelCase to snake_case\nname converter\n',
    'author': 'ThaRising',
    'author_email': 'kochbe.ber@gmail.com',
    'maintainer': 'Dominik Lewandowski',
    'maintainer_email': 'dominik.lewandow@gmail.com',
    'url': 'https://github.com/drizm-team/python-commons',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
