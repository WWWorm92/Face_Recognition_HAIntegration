from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import FaceRecognitionBridgeApi
from .const import CONF_API_TOKEN, CONF_BASE_URL, CONF_SCAN_INTERVAL, DOMAIN, PLATFORMS
from .coordinator import FaceRecognitionCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = FaceRecognitionBridgeApi(entry.data[CONF_BASE_URL], entry.data.get(CONF_API_TOKEN, ""))
    coordinator = FaceRecognitionCoordinator(hass, api, entry.data[CONF_SCAN_INTERVAL])
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
