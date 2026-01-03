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

    # ---------------------------
    # STEP 1 – SUPPLIER
    # ---------------------------
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            supplier = user_input["supplier"]
            self._data["supplier"] = supplier

            if supplier in SUPPLIER_PRESETS:
                self._data.update(SUPPLIER_PRESETS[supplier])

            return await self.async_step_energy()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("supplier", default="Electric Ireland"):
                    vol.In(list(SUPPLIER_PRESETS.keys()) + ["Other / Custom"])
            }),
            description_placeholders={
                "info": "Choose your electricity supplier. Tariffs can be customised later."
            },
        )

    # ---------------------------
    # STEP 2 – ENERGY SENSORS
    # ---------------------------
    async def async_step_energy(self, user_input=None):
        if user_input is not None:
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
