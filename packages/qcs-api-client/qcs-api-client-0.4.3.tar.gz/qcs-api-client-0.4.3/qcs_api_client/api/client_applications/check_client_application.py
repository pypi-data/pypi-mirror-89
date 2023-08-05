from typing import Any, Dict

import httpx
from retrying import retry

from ...models.check_client_application_request import CheckClientApplicationRequest
from ...models.check_client_application_response import CheckClientApplicationResponse
from ...types import Response
from ...util.errors import QCSHTTPStatusError, raise_for_status
from ...util.retry import DEFAULT_RETRY_ARGUMENTS


def _get_kwargs(
    *,
    json_body: CheckClientApplicationRequest,
) -> Dict[str, Any]:

    json_json_body = json_body.to_dict()

    return {
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> CheckClientApplicationResponse:
    raise_for_status(response)
    if response.status_code == 200:
        response_200 = CheckClientApplicationResponse.from_dict(response.json())

        return response_200
    else:
        raise QCSHTTPStatusError(
            f"Unexpected response: status code {response.status_code}", response=response, error=None
        )


def _build_response(*, response: httpx.Response) -> Response[CheckClientApplicationResponse]:
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
    json_body: CheckClientApplicationRequest,
) -> Response[CheckClientApplicationResponse]:
    url = "/v1/clientApplications:check"

    kwargs = _get_kwargs(
        json_body=json_body,
    )
    response = client.request(
        "post",
        url,
        **kwargs,
    )
    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
def sync_from_dict(
    *,
    client: httpx.Client,
    json_body_dict: Dict,
) -> Response[CheckClientApplicationResponse]:
    json_body = CheckClientApplicationRequest.from_dict(json_body_dict)

    url = "/v1/clientApplications:check"

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.request(
        "post",
        url,
        **kwargs,
    )

    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
async def asyncio(
    *,
    client: httpx.AsyncClient,
    json_body: CheckClientApplicationRequest,
) -> Response[CheckClientApplicationResponse]:
    url = "/v1/clientApplications:check"

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.request("post", url, **kwargs)

    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
async def asyncio_from_dict(
    *,
    client: httpx.AsyncClient,
    json_body_dict: Dict,
) -> Response[CheckClientApplicationResponse]:
    json_body = CheckClientApplicationRequest.from_dict(json_body_dict)

    url = "/v1/clientApplications:check"

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.request("post", url, **kwargs)

    return _build_response(response=response)
