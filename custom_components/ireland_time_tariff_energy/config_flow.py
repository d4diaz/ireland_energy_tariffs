from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "ireland_time_tariff_energy"

# ---------------------------
# SUPPLIER PRESETS (IRELAND)
# ---------------------------
SUPPLIER_PRESETS = {
    "Electric Ireland": {
        "night_start": "23:00",
        "day_start": "08:00",
        "peak_start": "17:00",
        "peak_end": "19:00",
        "import_night_rate": 0.18,
        "import_day_rate": 0.32,
        "import_peak_rate": 0.47,
        "export_night_rate": 0.18,
        "export_day_rate": 0.185,
        "export_peak_rate": 0.185,
    },
    "Energia": {
        "night_start": "23:00",
        "day_start": "08:00",
        "peak_start": "17:00",
        "peak_end": "19:00",
        "import_night_rate": 0.16,
        "import_day_rate": 0.29,
        "import_peak_rate": 0.44,
        "export_night_rate": 0.18,
        "export_day_rate": 0.18,
        "export_peak_rate": 0.18,
    },
    "Bord Gáis": {
        "night_start": "23:00",
        "day_start": "08:00",
        "peak_start": "17:00",
        "peak_end": "19:00",
        "import_night_rate": 0.17,
        "import_day_rate": 0.31,
        "import_peak_rate": 0.46,
        "export_night_rate": 0.18,
        "export_day_rate": 0.18,
        "export_peak_rate": 0.18,
    },
}


class IrelandTimeTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    # ---------------------------
    # STEP 1 – SUPPLIER
    # ---------------------------
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            supplier = user_input["supplier"]
            self._data["supplier"] = supplier

            if supplier in SUPPLIER_PRESETS:
                self._data.update(SUPPLIER_PRESETS[supplier])

            return await self.async_step_structure()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("supplier", default="Electric Ireland"):
                    vol.In(list(SUPPLIER_PRESETS.keys()) + ["Other / Custom"])
            }),
            description_placeholders={
                "info": "Select your electricity supplier (you can customise everything later)."
            },
        )

    # ---------------------------
    # STEP 2 – TARIFF STRUCTURE
    # ---------------------------
    async def async_step_structure(self, user_input=None):
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_times()

        return self.async_show_form(
            step_id="structure",
            data_schema=vol.Schema({
                vol.Required("has_weekend_rates", default=True): bool,
                vol.Required("has_peak_rates", default=True): bool,
                vol.Required("night_boost_enabled", default=False): bool,
            }),
            description_placeholders={
                "info": "Tell us how your electricity pricing is structured."
            },
        )

    # ---------------------------
    # STEP 3 – TIME PERIODS
    # ---------------------------
    async def async_step_times(self, user_input=None):
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_import_rates()

        fields = {
            vol.Required("night_start", default=self._data.get("night_start", "23:00")): str,
            vol.Required("day_start", default=self._data.get("day_start", "08:00")): str,
        }

        if self._data.get("has_peak_rates"):
            fields.update({
                vol.Required("peak_start", default=self._data.get("peak_start", "17:00")): str,
                vol.Required("peak_end", default=self._data.get("peak_end", "19:00")): str,
            })

        if self._data.get("night_boost_enabled"):
            fields.update({
                vol.Required("night_boost_start", default="02:00"): str,
                vol.Required("night_boost_end", default="04:00"): str,
            })

        return self.async_show_form(
            step_id="times",
            data_schema=vol.Schema(fields),
        )

    # ---------------------------
    # STEP 4 – IMPORT PRICES
    # ---------------------------
    async def async_step_import_rates(self, user_input=None):
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_export_rates()

        fields = {
            vol.Required(
                "import_night_rate",
                default=self._data.get("import_night_rate", 0.15)
            ): vol.Coerce(float),
            vol.Required(
                "import_day_rate",
                default=self._data.get("import_day_rate", 0.30)
            ): vol.Coerce(float),
        }

        if self._data.get("has_peak_rates"):
            fields[
                vol.Required(
                    "import_peak_rate",
                    default=self._data.get("import_peak_rate", 0.45)
                )
            ] = vol.Coerce(float)

        if self._data.get("has_weekend_rates"):
            fields.update({
                vol.Required("import_weekend_night_rate", default=0.14): vol.Coerce(float),
                vol.Required("import_weekend_day_rate", default=0.28): vol.Coerce(float),
            })

            if self._data.get("has_peak_rates"):
                fields[
                    vol.Required("import_weekend_peak_rate", default=0.40)
                ] = vol.Coerce(float)

        if self._data.get("night_boost_enabled"):
            fields[
                vol.Required("night_boost_import_rate", default=0.10)
            ] = vol.Coerce(float)

        return self.async_show_form(
            step_id="import_rates",
            data_schema=vol.Schema(fields),
        )

    # ---------------------------
    # STEP 5 – EXPORT PRICES
    # ---------------------------
    async def async_step_export_rates(self, user_input=None):
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(
                title="Ireland Time-Based Energy Tariffs",
                data=self._data,
            )

        fields = {
            vol.Required(
                "export_night_rate",
                default=self._data.get("export_night_rate", 0.12)
            ): vol.Coerce(float),
            vol.Required(
                "export_day_rate",
                default=self._data.get("export_day_rate", 0.185)
            ): vol.Coerce(float),
        }

        if self._data.get("has_peak_rates"):
            fields[
                vol.Required(
                    "export_peak_rate",
                    default=self._data.get("export_peak_rate", 0.25)
                )
            ] = vol.Coerce(float)

        if self._data.get("has_weekend_rates"):
            fields.update({
                vol.Required("export_weekend_night_rate", default=0.13): vol.Coerce(float),
                vol.Required("export_weekend_day_rate", default=0.20): vol.Coerce(float),
            })

            if self._data.get("has_peak_rates"):
                fields[
                    vol.Required("export_weekend_peak_rate", default=0.27)
                ] = vol.Coerce(float)

        if self._data.get("night_boost_enabled"):
            fields[
                vol.Required("night_boost_export_rate", default=0.30)
            ] = vol.Coerce(float)

        return self.async_show_form(
            step_id="export_rates",
            data_schema=vol.Schema(fields),
        )
vol.Required("grid_import_sensor"): selector.EntitySelector(
    selector.EntitySelectorConfig(
        domain="sensor",
        device_class="energy"
    )
)
entry.data["grid_import_sensor"]

vol.Optional("battery_discharge_sensor"):
    selector.EntitySelector(
        selector.EntitySelectorConfig(
            domain="sensor",
            device_class="energy"
        )
    )
entry.data["battery_discharge_sensor"]

