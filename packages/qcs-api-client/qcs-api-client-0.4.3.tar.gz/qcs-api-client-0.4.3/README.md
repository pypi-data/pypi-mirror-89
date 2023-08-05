# QCS API Client

A client library for accessing the Rigetti QCS API

## Usage

### Synchronous Usage

```python
from qcs_api_client.client.client import build_sync_client
from qcs_api_client.models import MyDatListReservationsResponseaModel
from qcs_api_client.operations.sync import list_reservations

with build_sync_client() as client:
    response: ListReservationsResponse = list_reservations(client=client)
```

### Asynchronous Usage

```python
from qcs_api_client.client.client import build_async_client
from qcs_api_client.models import ListReservationsResponse
from qcs_api_client.operations.asyncio import list_reservations

async with build_async_client() as client:
    response: ListReservationsResponse = await list_reservations(client=client)
```

1. Every path/method combo becomes a Python function with type annotations. 
2. All path/query params, and bodies become method arguments.
3. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
4. Any endpoint which did not have a tag will be in `qcs_api_client.api.default`
5. If the API returns a response code that was not declared in the OpenAPI document, a 
    `qcs_api_client.api.errors.ApiResponseError` wil be raised 
    with the `response` attribute set to the `httpx.Response` that was received.
