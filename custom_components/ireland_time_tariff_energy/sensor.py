from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ireland_time_tariff_energy"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
):
    async_add_entities([
        IrelandImportRateSensor(entry),
        IrelandExportRateSensor(entry),
    ])


class IrelandBaseRateSensor(SensorEntity):
    _attr_unit_of_measurement = "EUR/kWh"
    _attr_state_class = "measurement"
    _attr_device_class = "monetary"

    def __init__(self, entry: ConfigEntry):
        self.entry = entry


class IrelandImportRateSensor(IrelandBaseRateSensor):
    _attr_name = "Ireland Energy Import Rate"
    _attr_unique_id = "ireland_energy_import_rate"

    @property
    def native_value(self):
        # Temporary fixed value (safe baseline)
        return 0.30


class IrelandExportRateSensor(IrelandBaseRateSensor):
    _attr_name = "Ireland Energy Export Rate"
    _attr_unique_id = "ireland_energy_export_rate"

    @property
    def native_value(self):
        # Temporary fixed value (safe baseline)
        return 0.20
