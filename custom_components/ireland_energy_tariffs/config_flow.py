from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class IrelandEnergyTariffsConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN
):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Ireland Time Tariffs",
                data=user_input,
            )

        schema = vol.Schema({
    vol.Required("import_night_rate", default=0.15): float,
    vol.Required("import_day_rate", default=0.30): float,
    vol.Required("import_peak_rate", default=0.45): float,

    vol.Required("export_night_rate", default=0.12): float,
    vol.Required("export_day_rate", default=0.185): float,
    vol.Required("export_peak_rate", default=0.25): float,

    vol.Required("night_start", default="23:00"): str,
    vol.Required("day_start", default="08:00"): str,
    vol.Required("peak_start", default="17:00"): str,
    vol.Required("peak_end", default="19:00"): str,
})


        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
