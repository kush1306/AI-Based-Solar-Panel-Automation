from __future__ import annotations

import logging
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class ModelHttpClient:
    """Shared HTTP client for external AI model services."""

    def __init__(
        self,
        *,
        service_name: str,
        base_url: str,
        timeout_seconds: float,
    ) -> None:
        self.service_name = service_name
        self.base_url = base_url.rstrip("/")
        self.timeout = httpx.Timeout(timeout_seconds)

    async def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
        except httpx.TimeoutException as exc:
            logger.error("%s request timed out: %s", self.service_name, url)
            raise AppException(
                message=f"{self.service_name} timed out",
                status_code=504,
            ) from exc
        except httpx.RequestError as exc:
            logger.error("%s connection failed: %s | error=%s", self.service_name, url, exc)
            raise AppException(
                message=f"{self.service_name} is unavailable",
                status_code=503,
            ) from exc

        if response.status_code >= 400:
            logger.error(
                "%s returned HTTP %s for %s | body=%s",
                self.service_name,
                response.status_code,
                url,
                response.text,
            )
            raise AppException(
                message=f"{self.service_name} error (HTTP {response.status_code})",
                status_code=502 if response.status_code >= 500 else response.status_code,
            )

        try:
            payload = response.json()
        except Exception as exc:
            logger.exception("%s returned invalid JSON from %s", self.service_name, url)
            raise AppException(
                message=f"{self.service_name} returned invalid data",
                status_code=502,
            ) from exc

        if not isinstance(payload, dict):
            raise AppException(
                message=f"{self.service_name} returned unexpected payload",
                status_code=502,
            )

        return payload

    async def get_model(self, path: str, model: type[T], *, params: dict[str, Any] | None = None) -> T:
        payload = await self.get_json(path, params=params)
        try:
            return model.model_validate(payload)
        except Exception as exc:
            logger.exception("%s response validation failed for %s", self.service_name, path)
            raise AppException(
                message=f"{self.service_name} returned invalid data",
                status_code=502,
            ) from exc
