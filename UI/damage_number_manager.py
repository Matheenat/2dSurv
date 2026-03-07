from UI.damage_number import DamageNumber


class DamageNumberManager:
    def __init__(self, font):
        self.font = font
        self.numbers = []

    def spawn(self, x, y, value):
        self.numbers.append(DamageNumber(x, y, value, self.font))

    def update(self, dt):
        for number in self.numbers:
            number.update(dt)

        self.numbers = [n for n in self.numbers if n.is_alive()]

    def draw(self, screen, camera_offset):
        for number in self.numbers:
            number.draw(screen, camera_offset)