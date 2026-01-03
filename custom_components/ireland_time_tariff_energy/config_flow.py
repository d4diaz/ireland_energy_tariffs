from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN


class IrelandTimeTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Ireland Time Tariffs",
                data=user_input,
            )

        schema = vol.Schema({

            # --------------------
            # TIME DEFINITIONS
            # --------------------
            vol.Required("night_start", default="23:00"): str,
            vol.Required("day_start", default="08:00"): str,
            vol.Required("peak_start", default="17:00"): str,
            vol.Required("peak_end", default="19:00"): str,

            # --------------------
            # IMPORT – WEEKDAY
            # --------------------
            vol.Required("import_weekday_night_rate", default=0.15): float,
            vol.Required("import_weekday_day_rate", default=0.30): float,
            vol.Required("import_weekday_peak_rate", default=0.45): float,

            # --------------------
            # IMPORT – WEEKEND
            # --------------------
            vol.Required("import_weekend_night_rate", default=0.14): float,
            vol.Required("import_weekend_day_rate", default=0.28): float,
            vol.Required("import_weekend_peak_rate", default=0.40): float,

            # --------------------
            # EXPORT – WEEKDAY
            # --------------------
            vol.Required("export_weekday_night_rate", default=0.12): float,
            vol.Required("export_weekday_day_rate", default=0.185): float,
            vol.Required("export_weekday_peak_rate", default=0.25): float,

            # --------------------
            # EXPORT – WEEKEND
            # --------------------
            vol.Required("export_weekend_night_rate", default=0.13): float,
            vol.Required("export_weekend_day_rate", default=0.20): float,
            vol.Required("export_weekend_peak_rate", default=0.27): float,

            # --------------------
            # NIGHT BOOST (OPTIONAL)
            # --------------------
            vol.Optional("night_boost_enabled", default=False): bool,
            vol.Optional("night_boost_start", default="02:00"): str,
            vol.Optional("night_boost_end", default="04:00"): str,
            vol.Optional("night_boost_import_rate", default=0.10): float,
            vol.Optional("night_boost_export_rate", default=0.30): float,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
