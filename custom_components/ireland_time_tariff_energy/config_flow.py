from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "ireland_time_tariff_energy"


class IrelandTimeTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._config = {}

    # ---------------------------
    # STEP 1 – STRUCTURE
    # ---------------------------
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self._config.update(user_input)
            return await self.async_step_times()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("has_weekend_rates", default=True): bool,
                vol.Required("has_peak_rates", default=True): bool,
                vol.Required("night_boost_enabled", default=False): bool,
            }),
            description_placeholders={
                "info": "Select how your electricity tariffs are structured."
            },
        )

    # ---------------------------
    # STEP 2 – TIME PERIODS
    # ---------------------------
    async def async_step_times(self, user_input=None):
        if user_input is not None:
            self._config.update(user_input)
            return await self.async_step_import_rates()

        fields = {
            vol.Required("night_start", default="23:00"): str,
            vol.Required("day_start", default="08:00"): str,
        }

        if self._config["has_peak_rates"]:
            fields.update({
                vol.Required("peak_start", default="17:00"): str,
                vol.Required("peak_end", default="19:00"): str,
            })

        if self._config["night_boost_enabled"]:
            fields.update({
                vol.Required("night_boost_start", default="02:00"): str,
                vol.Required("night_boost_end", default="04:00"): str,
            })

        return self.async_show_form(
            step_id="times",
            data_schema=vol.Schema(fields),
        )

    # ---------------------------
    # STEP 3 – IMPORT PRICES
    # ---------------------------
    async def async_step_import_rates(self, user_input=None):
        if user_input is not None:
            self._config.update(user_input)
            return await self.async_step_export_rates()

        fields = {
            vol.Required("import_night_rate", default=0.15): vol.Coerce(float),
            vol.Required("import_day_rate", default=0.30): vol.Coerce(float),
        }

        if self._config["has_peak_rates"]:
            fields[vol.Required("import_peak_rate", default=0.45)] = vol.Coerce(float)

        if self._config["has_weekend_rates"]:
            fields.update({
                vol.Required("import_weekend_night_rate", default=0.14): vol.Coerce(float),
                vol.Required("import_weekend_day_rate", default=0.28): vol.Coerce(float),
            })

            if self._config["has_peak_rates"]:
                fields[vol.Required("import_weekend_peak_rate", default=0.40)] = vol.Coerce(float)

        if self._config["night_boost_enabled"]:
            fields[vol.Required("night_boost_import_rate", default=0.10)] = vol.Coerce(float)

        return self.async_show_form(
            step_id="import_rates",
            data_schema=vol.Schema(fields),
        )

    # ---------------------------
    # STEP 4 – EXPORT PRICES
    # ---------------------------
    async def async_step_export_rates(self, user_input=None):
        if user_input is not None:
            self._config.update(user_input)
            return self.async_create_entry(
                title="Ireland Time Tariffs",
                data=self._config,
            )

        fields = {
            vol.Required("export_night_rate", default=0.12): vol.Coerce(float),
            vol.Required("export_day_rate", default=0.185): vol.Coerce(float),
        }

        if self._config["has_peak_rates"]:
            fields[vol.Required("export_peak_rate", default=0.25)] = vol.Coerce(float)

        if self._config["has_weekend_rates"]:
            fields.update({
                vol.Required("export_weekend_night_rate", default=0.13): vol.Coerce(float),
                vol.Required("export_weekend_day_rate", default=0.20): vol.Coerce(float),
            })

            if self._config["has_peak_rates"]:
                fields[vol.Required("export_weekend_peak_rate", default=0.27)] = vol.Coerce(float)

        if self._config["night_boost_enabled"]:
            fields[vol.Required("night_boost_export_rate", default=0.30)] = vol.Coerce(float)

        return self.async_show_form(
            step_id="export_rates",
            data_schema=vol.Schema(fields),
        )
