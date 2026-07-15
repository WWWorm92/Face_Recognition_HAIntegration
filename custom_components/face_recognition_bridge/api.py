from __future__ import annotations

import requests


class FaceRecognitionBridgeApi:
    def __init__(self, base_url: str, api_token: str = "", timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token.strip()
        self.timeout = timeout

    def get_health(self) -> dict:
        return self._get("/health")

    def get_latest_event(self) -> dict:
        return self._get("/events/latest")

    def _get(self, path: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else None
        response = requests.get(f"{self.base_url}{path}", timeout=self.timeout, headers=headers)
        response.raise_for_status()
        return response.json()
