import pygame
from pygame.math import Vector2

class Timer:
    def __init__(self, max):
        self.count = 0
        self.max = max
        self.stopped = True

    def start(self):
        self.count = 1
        self.stopped = False

    def stop(self):
        self.stopped = True

    def reset(self):
        self.count = 0
        self.stopped = True

    def tick(self):
        if self.count >= self.max:
            self.reset()
        if not self.stopped:
            self.count += 1

class Circular_Hitbox(Vector2):
    def __init__(self, position, radius):
        self.update(position)
        self.r = radius

    def detect_collision(self, hitbox):
        if self.distance_to(hitbox) <= (self.r + hitbox.r)*1.00:
            return True
        else:
            return False

class Planet(pygame.sprite.Sprite):
    def __init__(self, position, radius, mass=0, bounciness=.5):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        color = 255*(mass-1000)/3000
        pygame.draw.circle(self.image, (int(color),(255-color),0), (radius,radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.hitbox = Circular_Hitbox(position, radius)

        self.position = Vector2(position)
        self.radius = radius
        self.mass = mass
        self.density = self.mass/self.radius
        self.bounciness = bounciness

class Circular_Sprite_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        for sprite in self:
            sprite.rect.x, sprite.rect.y = sprite.hitbox.x-sprite.hitbox.r, sprite.hitbox.y-sprite.hitbox.r
        super().draw(screen)

class Golfball(pygame.sprite.Sprite):
    def __init__(self, position, planets, radius=7, initial_velocity=(0,0), hit_power=50, **kwargs):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(self.image, (255,255,255), (radius,radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.hitbox = Circular_Hitbox(position, radius)

        self.position = Vector2(position)
        self.inital_position = Vector2(position)
        self.last_position = Vector2(position)

        self.initial_velocity = Vector2(initial_velocity)
        self.velocity = Vector2(initial_velocity)
        self.acceleration = Vector2(0)
        self.hit_power = hit_power
        self.planets = planets
        self.timers = {'surface_timer': Timer(max=10), 'no_collide': Timer(max=5)}

        self.strokes = 0

        self.on_surface = False
        self.launching = False

    def reset_ball(self):
        self.position = self.inital_position
        self.velocity = self.initial_velocity
        self.acceleration = Vector2(0)

    def launch(self):
        self.last_position = self.position
        mouse_pos = Vector2(pygame.mouse.get_pos())
        self.velocity = (self.position - mouse_pos)/7
        self.velocity.scale_to_length(self.position.distance_to(mouse_pos)*self.hit_power/300)
        if self.velocity.magnitude() > self.hit_power:
            self.velocity.scale_to_length(self.hit_power)
        self.timers['surface_timer'].reset()
        self.timers['no_collide'].start()
        self.strokes += 1

    def gravity(self):
        self.acceleration.update(0)
        for planet in self.planets:
            acceleration_magnitude = planet.mass/(self.position.distance_to(planet.position)**2)
            g = (planet.position - self.position)
            g.scale_to_length(acceleration_magnitude)
            self.acceleration += g

    def collisions(self):
        for planet in self.planets:
            if self.hitbox.detect_collision(planet.hitbox):
                if not self.timers['surface_timer'].stopped:
                    self.timers['surface_timer'].stop()
                    self.acceleration.update(0)
                    self.velocity.update(0)
                    self.position = planet.position - (planet.position - self.position).normalize()*(planet.hitbox.r + self.hitbox.r)
                else:
                    self.acceleration.update(0)
                    self.velocity.reflect_ip(planet.position - self.position)
                    self.velocity *= planet.bounciness
                    self.position = planet.position - (planet.position - self.position).normalize()*(planet.hitbox.r + self.hitbox.r)
                    self.timers['surface_timer'].start()

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.hitbox.x = self.position.x
        self.hitbox.y = self.position.y

    def update(self):
        for name in self.timers:
            self.timers[name].tick()
        self.gravity()
        if self.timers['no_collide'].stopped:
            self.collisions()
        self.move()
