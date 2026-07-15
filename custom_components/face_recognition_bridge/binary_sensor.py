from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .entity import FaceRecognitionEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KnownFaceDetectedBinarySensor(coordinator, entry), UnknownFaceDetectedBinarySensor(coordinator, entry)])


class KnownFaceDetectedBinarySensor(FaceRecognitionEntity, BinarySensorEntity):
    _attr_name = "Face Recognition Known Detected"

    @property
    def is_on(self):
        event = self.coordinator.data.get("latest_event", {})
        return bool(event.get("event_id")) and bool(event.get("matched"))


class UnknownFaceDetectedBinarySensor(FaceRecognitionEntity, BinarySensorEntity):
    _attr_name = "Face Recognition Unknown Detected"

    @property
    def is_on(self):
        event = self.coordinator.data.get("latest_event", {})
        return bool(event.get("event_id")) and not bool(event.get("matched"))
