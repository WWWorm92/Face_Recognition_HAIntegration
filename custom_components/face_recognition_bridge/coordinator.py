from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import FaceRecognitionBridgeApi
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


class FaceRecognitionCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: FaceRecognitionBridgeApi, interval_seconds: int) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=interval_seconds))
        self.api = api
        self.last_event_id: str | None = None

    async def _async_update_data(self) -> dict:
        try:
            health = await self.hass.async_add_executor_job(self.api.get_health)
            latest_event = await self.hass.async_add_executor_job(self.api.get_latest_event)
        except Exception as exc:
            raise UpdateFailed(str(exc)) from exc

        event_id = latest_event.get("event_id")
        if event_id and event_id != self.last_event_id:
            self.last_event_id = event_id
            event_type = "face_recognition_match" if latest_event.get("matched") else "face_recognition_unknown"
            self.hass.bus.async_fire(event_type, latest_event)

        return {"health": health, "latest_event": latest_event}
