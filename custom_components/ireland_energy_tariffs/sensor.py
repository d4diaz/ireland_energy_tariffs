from datetime import datetime
from homeassistant.components.sensor import SensorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        ImportRateSensor(entry),
        ExportRateSensor(entry),
    ])
async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        ImportRateSensor(entry),
        ExportRateSensor(entry),
    ])



class BaseRateSensor(SensorEntity):
    _attr_unit_of_measurement = "EUR/kWh"
    _attr_device_class = "monetary"
    _attr_state_class = "measurement"

    def __init__(self, entry):
        self.entry = entry

    def _current_period(self):
        now = datetime.now().time()

        night_start = datetime.strptime(self.entry.data["night_start"], "%H:%M").time()
        day_start = datetime.strptime(self.entry.data["day_start"], "%H:%M").time()
        peak_start = datetime.strptime(self.entry.data["peak_start"], "%H:%M").time()
        peak_end = datetime.strptime(self.entry.data["peak_end"], "%H:%M").time()

        if peak_start <= now < peak_end:
            return "peak"
        elif day_start <= now < night_start:
            return "day"
        else:
            return "night"

class ImportRateSensor(BaseRateSensor):
    _attr_name = "Ireland Energy Import Rate"
    _attr_unique_id = "ireland_energy_import_rate"

    @property
    def native_value(self):
        period = self._current_period()

        return self.entry.data[f"import_{period}_rate"]


class ExportRateSensor(BaseRateSensor):
    _attr_name = "Ireland Energy Export Rate"
    _attr_unique_id = "ireland_energy_export_rate"

    @property
    def native_value(self):
        period = self._current_period()

        return self.entry.data[f"export_{period}_rate"]

