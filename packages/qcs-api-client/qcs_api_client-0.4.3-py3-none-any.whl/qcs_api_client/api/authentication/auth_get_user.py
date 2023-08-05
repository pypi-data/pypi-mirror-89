from typing import Any, Dict

import httpx
from retrying import retry

from ...models.user import User
from ...types import Response
from ...util.errors import QCSHTTPStatusError, raise_for_status
from ...util.retry import DEFAULT_RETRY_ARGUMENTS


def _get_kwargs() -> Dict[str, Any]:

    return {}


def _parse_response(*, response: httpx.Response) -> User:
    raise_for_status(response)
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

        return response_200
    else:
        raise QCSHTTPStatusError(
            f"Unexpected response: status code {response.status_code}", response=response, error=None
        )


def _build_response(*, response: httpx.Response) -> Response[User]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


@retry(**DEFAULT_RETRY_ARGUMENTS)
def sync(
    *,
    client: httpx.Client,
) -> Response[User]:
    url = "/v1/auth:getUser"

    kwargs = _get_kwargs()
    response = client.request(
        "get",
        url,
        **kwargs,
    )
    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
def sync_from_dict(
    *,
    client: httpx.Client,
) -> Response[User]:

    url = "/v1/auth:getUser"

    kwargs = _get_kwargs()

    response = client.request(
        "get",
        url,
        **kwargs,
    )

    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
async def asyncio(
    *,
    client: httpx.AsyncClient,
) -> Response[User]:
    url = "/v1/auth:getUser"

    kwargs = _get_kwargs()

    response = await client.request("get", url, **kwargs)

    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
async def asyncio_from_dict(
    *,
    client: httpx.AsyncClient,
) -> Response[User]:

    url = "/v1/auth:getUser"

    kwargs = _get_kwargs()

    response = await client.request("get", url, **kwargs)

    return _build_response(response=response)
