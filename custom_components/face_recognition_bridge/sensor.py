from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .entity import FaceRecognitionEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            LastPersonSensor(coordinator, entry),
            LastCameraSensor(coordinator, entry),
            LastScoreSensor(coordinator, entry),
        ]
    )


class LastPersonSensor(FaceRecognitionEntity, SensorEntity):
    _attr_name = "Face Recognition Last Person"

    @property
    def native_value(self):
        return self.coordinator.data.get("latest_event", {}).get("person_name")


class LastCameraSensor(FaceRecognitionEntity, SensorEntity):
    _attr_name = "Face Recognition Last Camera"

    @property
    def native_value(self):
        return self.coordinator.data.get("latest_event", {}).get("source_name")


class LastScoreSensor(FaceRecognitionEntity, SensorEntity):
    _attr_name = "Face Recognition Last Score"

    @property
    def native_value(self):
        return self.coordinator.data.get("latest_event", {}).get("score")
