
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        return {
            "building": self.name,
            "total": self.calculate_total_consumption(),
            "count": len(self.meter_readings)
        }

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_building(self, building):
        self.buildings[building.name] = building

    def campus_summary(self):
        return {name: b.generate_report() for name, b in self.buildings.items()}
