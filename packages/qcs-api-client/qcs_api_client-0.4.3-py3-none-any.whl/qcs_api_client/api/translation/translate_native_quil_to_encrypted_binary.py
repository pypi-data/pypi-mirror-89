from typing import Any, Dict

import httpx
from retrying import retry

from ...models.translate_native_quil_to_encrypted_binary_request import TranslateNativeQuilToEncryptedBinaryRequest
from ...models.translate_native_quil_to_encrypted_binary_response import TranslateNativeQuilToEncryptedBinaryResponse
from ...types import Response
from ...util.errors import QCSHTTPStatusError, raise_for_status
from ...util.retry import DEFAULT_RETRY_ARGUMENTS


def _get_kwargs(
    *,
    quantum_processor_id: str,
    json_body: TranslateNativeQuilToEncryptedBinaryRequest,
) -> Dict[str, Any]:

    json_json_body = json_body.to_dict()

    return {
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> TranslateNativeQuilToEncryptedBinaryResponse:
    raise_for_status(response)
    if response.status_code == 200:
        response_200 = TranslateNativeQuilToEncryptedBinaryResponse.from_dict(response.json())

        return response_200
    else:
        raise QCSHTTPStatusError(
            f"Unexpected response: status code {response.status_code}", response=response, error=None
        )


def _build_response(*, response: httpx.Response) -> Response[TranslateNativeQuilToEncryptedBinaryResponse]:
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
    json_body: TranslateNativeQuilToEncryptedBinaryRequest,
) -> Response[TranslateNativeQuilToEncryptedBinaryResponse]:
    url = "/v1/quantumProcessors/{quantumProcessorId}:translateNativeQuilToEncryptedBinary".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
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
    quantum_processor_id: str,
    json_body_dict: Dict,
) -> Response[TranslateNativeQuilToEncryptedBinaryResponse]:
    json_body = TranslateNativeQuilToEncryptedBinaryRequest.from_dict(json_body_dict)

    url = "/v1/quantumProcessors/{quantumProcessorId}:translateNativeQuilToEncryptedBinary".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
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
    quantum_processor_id: str,
    json_body: TranslateNativeQuilToEncryptedBinaryRequest,
) -> Response[TranslateNativeQuilToEncryptedBinaryResponse]:
    url = "/v1/quantumProcessors/{quantumProcessorId}:translateNativeQuilToEncryptedBinary".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
        json_body=json_body,
    )

    response = await client.request("post", url, **kwargs)

    return _build_response(response=response)


@retry(**DEFAULT_RETRY_ARGUMENTS)
async def asyncio_from_dict(
    *,
    client: httpx.AsyncClient,
    quantum_processor_id: str,
    json_body_dict: Dict,
) -> Response[TranslateNativeQuilToEncryptedBinaryResponse]:
    json_body = TranslateNativeQuilToEncryptedBinaryRequest.from_dict(json_body_dict)

    url = "/v1/quantumProcessors/{quantumProcessorId}:translateNativeQuilToEncryptedBinary".format(
        quantumProcessorId=quantum_processor_id,
    )

    kwargs = _get_kwargs(
        quantum_processor_id=quantum_processor_id,
        json_body=json_body,
    )

    response = await client.request("post", url, **kwargs)

    return _build_response(response=response)
