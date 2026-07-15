from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity


class FaceRecognitionEntity(CoordinatorEntity):
    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator)
        self.entry = entry
