from datetime import datetime
from homeassistant.components.sensor import SensorEntity

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

    def _is_day(self):
        now = datetime.now().time()
        day_start = datetime.strptime(self.entry.data["day_start"], "%H:%M").time()
        night_start = datetime.strptime(self.entry.data["night_start"], "%H:%M").time()
        return day_start <= now < night_start

class ImportRateSensor(BaseRateSensor):
    _attr_name = "Ireland Energy Import Rate"
    _attr_unique_id = "ireland_energy_import_rate"

    @property
    def native_value(self):
        return (
            self.entry.data["import_day_rate"]
            if self._is_day()
            else self.entry.data["import_night_rate"]
        )

class ExportRateSensor(BaseRateSensor):
    _attr_name = "Ireland Energy Export Rate"
    _attr_unique_id = "ireland_energy_export_rate"

    @property
    def native_value(self):
        return (
            self.entry.data["export_day_rate"]
            if self._is_day()
            else self.entry.data["export_night_rate"]
        )
