import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

DOMAIN = "ireland_time_tariff_energy"

SUPPLIER_PRESETS = {
    "Electric Ireland": {
        "night_start": "23:00",
        "day_start": "08:00",
        "peak_start": "17:00",
        "peak_end": "19:00",
        "import_night_rate": 0.18,
        "import_day_rate": 0.32,
        "import_peak_rate": 0.47,
        "export_day_rate": 0.185,
    },
    "Energia": {
        "night_start": "23:00",
        "day_start": "08:00",
        "peak_start": "17:00",
        "peak_end": "19:00",
        "import_night_rate": 0.16,
        "import_day_rate": 0.29,
        "import_peak_rate": 0.44,
        "export_day_rate": 0.18,
    },
    "Bord Gáis": {
        "night_start": "23:00",
        "day_start": "08:00",
        "peak_start": "17:00",
        "peak_end": "19:00",
        "import_night_rate": 0.17,
        "import_day_rate": 0.31,
        "import_peak_rate": 0.46,
        "export_day_rate": 0.18,
    },
}


class IrelandTimeTariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    async def async_step_user(self, user_input=None):
        if user_input:
            supplier = user_input["supplier"]
            self._data["supplier"] = supplier

            if supplier in SUPPLIER_PRESETS:
                self._data.update(SUPPLIER_PRESETS[supplier])

            return await self.async_step_energy()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("supplier", default="Electric Ireland"):
                    vol.In(list(SUPPLIER_PRESETS) + ["Other / Custom"])
            }),
        )

    async def async_step_energy(self, user_input=None):
        if user_input:
            self._data.update(user_input)
            return self.async_create_entry(
                title="Ireland Time-Based Energy Tariffs",
                data=self._data,
            )

        return self.async_show_form(
            step_id="energy",
            data_schema=vol.Schema({
                vol.Required("grid_import_sensor"):
                    selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            device_class="energy"
                        )
                    ),
                vol.Optional("battery_discharge_sensor"):
                    selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            device_class="energy"
                        )
                    ),
            }),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return IrelandTimeTariffOptionsFlow(config_entry)


class IrelandTimeTariffOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input:
            return self.async_create_entry(title="", data=user_input)

        def opt(key, default):
            return self.entry.options.get(key, self.entry.data.get(key, default))

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("import_day_rate", default=opt("import_day_rate", 0.30)):
                    vol.Coerce(float),
                vol.Required("import_night_rate", default=opt("import_night_rate", 0.15)):
                    vol.Coerce(float),
                vol.Required("import_peak_rate", default=opt("import_peak_rate", 0.45)):
                    vol.Coerce(float),
                vol.Required("export_day_rate", default=opt("export_day_rate", 0.18)):
                    vol.Coerce(float),
            }),
        )
