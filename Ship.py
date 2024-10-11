

class Ship:
    def __init__(self, x, y, speed, max_hp):
        self.x = x
        self.y = y
        self.hull_hp = max_hp
        self.hull_max_hp = max_hp
        self.hull_text = None
        self.speed = speed
        self.speed_text = None
        self.core = None
        self.shield = None



class ShipCore:
    def __init__(self, base_output, max_energy):
        self.base_output = base_output
        self.output = base_output
        self.energy = max_energy
        self.max_energy = max_energy
        self.output_text = None
        self.energy_text = None


class ShipShields:
    def __init__(self, max_shield_level):
        self.delta = 0.0
        self.level = max_shield_level
        self.max = max_shield_level
        self.delta_text = None
        self.shield_text = None
        self.max_text = None
        self.max_delta = 0.5