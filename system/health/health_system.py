class HealthSystem:
    def __init__(self, max_hp, invincible_duration=500):
        self.max_hp = max_hp
        self.hp = max_hp

        self.invincible_duration = invincible_duration
        self.invincible_timer = 0

        self.dead = False

    def take_damage(self, amount):
        if self.dead:
            return

        if self.invincible_timer > 0:
            return

        self.hp -= amount
        self.invincible_timer = self.invincible_duration

        if self.hp <= 0:
            self.hp = 0
            self.dead = True

    def heal(self, amount):
        if self.dead:
            return

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def update(self, dt):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer < 0:
                self.invincible_timer = 0