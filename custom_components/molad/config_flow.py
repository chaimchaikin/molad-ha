from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN


class MoladConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, info):
        return self.async_create_entry(title="Molad", data={})
