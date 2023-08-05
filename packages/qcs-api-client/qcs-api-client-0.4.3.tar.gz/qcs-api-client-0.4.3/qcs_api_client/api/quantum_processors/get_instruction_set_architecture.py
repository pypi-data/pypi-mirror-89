from typing import Any, Dict

import httpx
from retrying import retry

from ...models.instruction_set_architecture import InstructionSetArchitecture
from ...types import Response
from ...util.errors import QCSHTTPStatusError, raise_for_status
from ...util.retry import DEFAULT_RETRY_ARGUMENTS


def _get_kwargs(
    *,
    quantum_processor_id: str,
) -> Dict[str, Any]:

    return {}


def _parse_response(*, response: httpx.Response) -> InstructionSetArchitecture:
    raise_for_status(response)
    if response.status_code == 200:
        response_200 = InstructionSetArchitecture.from_dict(response.json())

        return response_200
    else:
        raise QCSHTTPStatusError(
            f"Unexpected response: status code {response.status_code}", response=response, error=None
        )


def _build_response(*, response: httpx.Response) -> Response[InstructionSetArchitecture]:
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
    quantum_processor_id: str,
) -> Response[InstructionSetArchitecture]:
    url = "/v1/quantumProcessors/{quantumProcessorId}/instructionSetArchitecture".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
    )
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
    quantum_processor_id: str,
) -> Response[InstructionSetArchitecture]:

    url = "/v1/quantumProcessors/{quantumProcessorId}/instructionSetArchitecture".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
    )

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
    quantum_processor_id: str,
) -> Response[InstructionSetArchitecture]:
    url = "/v1/quantumProcessors/{quantumProcessorId}/instructionSetArchitecture".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
    )

    response = await client.request("get", url, **kwargs)

    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
async def asyncio_from_dict(
    *,
    client: httpx.AsyncClient,
    quantum_processor_id: str,
) -> Response[InstructionSetArchitecture]:

    url = "/v1/quantumProcessors/{quantumProcessorId}/instructionSetArchitecture".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
    )

    response = await client.request("get", url, **kwargs)

    return _build_response(response=response)
