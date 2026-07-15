from __future__ import annotations

from aiohttp import ClientError
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class FaceRecognitionBridgeApi:
    def __init__(self, hass, base_url: str, api_token: str = "", timeout: int = 10) -> None:
        self.hass = hass
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token.strip()
        self.timeout = timeout

    async def get_health(self) -> dict:
        return await self._get("/health")

    async def get_latest_event(self) -> dict:
        return await self._get("/events/latest")

    async def _get(self, path: str) -> dict:
        session = async_get_clientsession(self.hass)
        headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else None
        try:
            async with session.get(f"{self.base_url}{path}", timeout=self.timeout, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except ClientError as error:
            raise RuntimeError(str(error)) from error
