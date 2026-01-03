class DailyCostSensor(SensorEntity):
    _attr_state_class = "total"
    _attr_device_class = "monetary"
    _attr_unit_of_measurement = "EUR"

    def __init__(self, source_sensor, cycle):
        self.source_sensor = source_sensor
        self.cycle = cycle

    async def async_update(self):
        # reset at midnight / month start
