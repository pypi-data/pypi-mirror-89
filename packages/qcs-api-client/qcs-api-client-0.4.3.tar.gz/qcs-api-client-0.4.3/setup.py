# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcs_api_client',
 'qcs_api_client.api',
 'qcs_api_client.api.authentication',
 'qcs_api_client.api.client_applications',
 'qcs_api_client.api.default',
 'qcs_api_client.api.endpoints',
 'qcs_api_client.api.engagements',
 'qcs_api_client.api.quantum_processors',
 'qcs_api_client.api.reservations',
 'qcs_api_client.api.translation',
 'qcs_api_client.client',
 'qcs_api_client.client._configuration',
 'qcs_api_client.models',
 'qcs_api_client.operations.asyncio',
 'qcs_api_client.operations.asyncio_from_dict',
 'qcs_api_client.operations.sync',
 'qcs_api_client.operations.sync_from_dict',
 'qcs_api_client.util']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'httpx>=0.15.0,<0.16.0',
 'iso8601>=0.1.13,<0.2.0',
 'pydantic>=1.7.2,<2.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'retrying>=1.3.3,<2.0.0',
 'rfc3339>=6.2,<7.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'qcs-api-client',
    'version': '0.4.3',
    'description': 'A client library for accessing the Rigetti QCS API',
    'long_description': '# QCS API Client\n\nA client library for accessing the Rigetti QCS API\n\n## Usage\n\n### Synchronous Usage\n\n```python\nfrom qcs_api_client.client.client import build_sync_client\nfrom qcs_api_client.models import MyDatListReservationsResponseaModel\nfrom qcs_api_client.operations.sync import list_reservations\n\nwith build_sync_client() as client:\n    response: ListReservationsResponse = list_reservations(client=client)\n```\n\n### Asynchronous Usage\n\n```python\nfrom qcs_api_client.client.client import build_async_client\nfrom qcs_api_client.models import ListReservationsResponse\nfrom qcs_api_client.operations.asyncio import list_reservations\n\nasync with build_async_client() as client:\n    response: ListReservationsResponse = await list_reservations(client=client)\n```\n\n1. Every path/method combo becomes a Python function with type annotations. \n2. All path/query params, and bodies become method arguments.\n3. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n4. Any endpoint which did not have a tag will be in `qcs_api_client.api.default`\n5. If the API returns a response code that was not declared in the OpenAPI document, a \n    `qcs_api_client.api.errors.ApiResponseError` wil be raised \n    with the `response` attribute set to the `httpx.Response` that was received.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
