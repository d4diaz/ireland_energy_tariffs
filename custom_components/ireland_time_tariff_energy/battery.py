from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN


# --------------------------------------------------
# SETUP
# --------------------------------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
):
    entities = []

    # Battery discharge sensor is optional
    discharge_sensor = entry.data.get("battery_discharge_sensor")
    if discharge_sensor:
        entities.append(BatterySavingsSensor(hass, entry))
        entities.append(PeakAvoidanceSavingsSensor(hass, entry))

    if entities:
        async_add_entities(entities)
        for entity in entities:
            await entity.async_start_listening()


# --------------------------------------------------
# BASE BATTERY SAVINGS SENSOR
# --------------------------------------------------
class BaseBatterySavingsSensor(SensorEntity):
    _attr_unit_of_measurement = "EUR"
    _attr_device_class = "monetary"
    _attr_state_class = "total_increasing"
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self._attr_native_value = 0.0

        self._last_energy = None

        self.discharge_sensor = entry.data["battery_discharge_sensor"]
        self.import_rate_sensor = "sensor.ireland_energy_import_rate"

    async def async_added_to_hass(self):
        # Restore previous value after restart
        state = self.hass.states.get(self.entity_id)
        if state and state.state not in ("unknown", "unavailable"):
            try:
                self._attr_native_value = float(state.state)
            except ValueError:
                self._attr_native_value = 0.0

    async def async_start_listening(self):
        async_track_state_change_event(
            self.hass,
            self.discharge_sensor,
            self._handle_discharge_change,
        )

    @callback
    def _handle_discharge_change(self, event):
        new_state = event.data.get("new_state")
        if not new_state or new_state.state in ("unknown", "unavailable"):
            return

        try:
            energy = float(new_state.state)
        except ValueError:
            return

        # First update – initialise
        if self._last_energy is None:
            self._last_energy = energy
            return

        delta_kwh = energy - self._last_energy
        self._last_energy = energy

        # Only count discharge increases
        if delta_kwh <= 0:
            return

        # Check if this savings sensor should be active
        if not self._is_active_period():
            return

        rate_state = self.hass.states.get(self.import_rate_sensor)
        if not rate_state or rate_state.state in ("unknown", "unavailable"):
            return

        try:
            rate = float(rate_state.state)
        except ValueError:
            return

        self._attr_native_value += delta_kwh * rate
        self.async_write_ha_state()

    def _is_active_period(self) -> bool:
        """Override in subclasses"""
        return False


# --------------------------------------------------
# TOTAL BATTERY SAVINGS
# --------------------------------------------------
class BatterySavingsSensor(BaseBatterySavingsSensor):
    _attr_name = "Battery Savings"
    _attr_unique_id = "battery_savings_total"

    def _is_active_period(self) -> bool:
        # Battery savings apply in ALL periods
        return True


# --------------------------------------------------
# PEAK AVOIDANCE SAVINGS
# --------------------------------------------------
class PeakAvoidanceSavingsSensor(BaseBatterySavingsSensor):
    _attr_name = "Peak Avoidance Savings"
    _attr_unique_id = "battery_peak_avoidance_savings"

    def _is_active_period(self) -> bool:
        rate_state = self.hass.states.get(self.import_rate_sensor)
        if not rate_state:
            return False

        return rate_state.attributes.get("current_period") == "peak"
