from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .api import FaceRecognitionBridgeApi
from .const import CONF_API_TOKEN, CONF_BASE_URL, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN


class FaceRecognitionBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            normalized_url = user_input[CONF_BASE_URL].rstrip("/")
            await self.async_set_unique_id(normalized_url)
            self._abort_if_unique_id_configured()

            api = FaceRecognitionBridgeApi(self.hass, normalized_url, user_input.get(CONF_API_TOKEN, ""))
            try:
                await api.get_health()
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                user_input[CONF_BASE_URL] = normalized_url
                return self.async_create_entry(title="Face Recognition Bridge", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_BASE_URL): str,
                vol.Optional(CONF_API_TOKEN, default=""): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
