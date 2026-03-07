class HealthSystem:
    def __init__(self, max_hp, invincible_duration=500):
        self.max_hp = max_hp
        self.hp = max_hp

        self.invincible_duration = invincible_duration
        self.invincible_timer = 0

        self.dead = False

        self.just_took_damage = False
        self.last_damage_amount = 0

    def take_damage(self, amount):
        if self.dead:
            return False

        if self.invincible_timer > 0:
            return False

        self.hp -= amount
        self.invincible_timer = self.invincible_duration

        self.just_took_damage = True
        self.last_damage_amount = amount

        if self.hp <= 0:
            self.hp = 0
            self.dead = True

        return True

    def heal(self, amount):
        if self.dead:
            return

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def update(self, dt):
        self.just_took_damage = False

        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer < 0:
                self.invincible_timer = 0

    def get_hp_ratio(self):
        if self.max_hp <= 0:
            return 0
        return self.hp / self.max_hp

    def is_invincible(self):
        return self.invincible_timer > 0