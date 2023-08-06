# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fhiry']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.1.4']

setup_kwargs = {
    'name': 'fhiry',
    'version': '0.5.0',
    'description': 'FHIR to pd.Dataframe',
    'long_description': "# :fire: fhiry - FHIR for AI and ML\n\n## About\n\n[Bulk data export using FHIR](https://hl7.org/fhir/uv/bulkdata/export/index.html) may be important if you want to export a cohort for analysis or machine learning.\n:fire: **Fhiry** is a python package to facilitate this by converting a folder of FHIR bundles/ndjson into a pandas data frame for analysis and importing\ninto ML packages such as Tensorflow and PyTorch. Test it with the [synthea sample](https://synthea.mitre.org/downloads). Use the 'Discussions' tab above for feature requests.\n\n## Installation\n\n```\npip install fhiry\n```\n\n## Usage\n\n### Synthea\n\n```\nimport fhiry.parallel as fp\ndf = fp.process('/path/to/fhir/resources')\nprint(df.info())\n```\n\n### [SMART Bulk Data Server](https://bulk-data.smarthealthit.org/) Export\n```\nimport fhiry.parallel as fp\ndf = fp.ndjson('/path/to/fhir/ndjson/files')\nprint(df.info())\n```\n## Columns\n* see df.columns\n\n```\npatientId\nfullUrl\nresource.resourceType\nresource.id\nresource.name\nresource.telecom\nresource.gender\n...\n...\n...\n```\n\n### [Modules](https://dermatologist.github.io/fhiry/build/html/modules.html)\n## Contributors\n\n* [Bell Eapen](https://nuchange.ca)\n* WIP, PR welcome, please see CONTRIBUTING.md\n* [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg) using CC](https://computecanada.ca)\n",
    'author': 'Bell Eapen',
    'author_email': 'github@gulfdoctor.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dermatologist/fhiry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
