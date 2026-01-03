from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ireland_time_tariff_energy"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities(
        [
            IrelandImportRateSensor(entry),
            IrelandExportRateSensor(entry),
        ]
    )


class IrelandBaseRateSensor(SensorEntity):
    _attr_unit_of_measurement = "EUR/kWh"
    _attr_device_class = "monetary"
    _attr_state_class = "measurement"
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry):
        self.entry = entry

    # ---------- helpers ----------
    def _now(self):
        return datetime.now().time()

    def _parse(self, value):
        return datetime.strptime(value, "%H:%M").time()

    def _cfg(self, key, default=None):
        """Read from options first, fallback to data"""
        return self.entry.options.get(key, self.entry.data.get(key, default))

    def _is_weekend(self):
        return datetime.now().weekday() >= 5

    def _current_period(self):
        now = self._now()

        night_start = self._parse(self._cfg("night_start", "23:00"))
        day_start = self._parse(self._cfg("day_start", "08:00"))

        if self._cfg("has_peak_rates", False):
            peak_start = self._parse(self._cfg("peak_start", "17:00"))
            peak_end = self._parse(self._cfg("peak_end", "19:00"))
            if peak_start <= now < peak_end:
                return "peak"

        if day_start <= now < night_start:
            return "day"

        return "night"

    def _night_boost_active(self):
        if not self._cfg("night_boost_enabled", False):
            return False

        now = self._now()
        start = self._parse(self._cfg("night_boost_start", "02:00"))
        end = self._parse(self._cfg("night_boost_end", "04:00"))

        return start <= now < end

    @property
    def extra_state_attributes(self):
        return {
            "current_period": self._current_period(),
            "is_weekend": self._is_weekend(),
            "night_boost_active": self._night_boost_active(),
        }


class IrelandImportRateSensor(IrelandBaseRateSensor):
    _attr_name = "Ireland Energy Import Rate"
    _attr_unique_id = "ireland_energy_import_rate"

    @property
    def native_value(self):
        if self._night_boost_active():
            return self._cfg("night_boost_import_rate", 0)

        period = self._current_period()

        if self._cfg("has_weekend_rates", False):
            day_type = "weekend" if self._is_weekend() else "weekday"
            return self._cfg(f"import_{day_type}_{period}_rate", 0)

        return self._cfg(f"import_{period}_rate", 0)


class IrelandExportRateSensor(IrelandBaseRateSensor):
    _attr_name = "Ireland Energy Export Rate"
    _attr_unique_id = "ireland_energy_export_rate"

    @property
    def native_value(self):
        if self._night_boost_active():
            return self._cfg("night_boost_export_rate", 0)

        period = self._current_period()

        if self._cfg("has_weekend_rates", False):
            day_type = "weekend" if self._is_weekend() else "weekday"
            return self._cfg(f"export_{day_type}_{period}_rate", 0)

        return self._cfg(f"export_{period}_rate", 0)
