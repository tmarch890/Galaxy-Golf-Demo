import pygame
import code.objects
import code.input
import random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

planet1 = code.objects.Planet((random.randint(200,1000), random.randint(200,1000)), radius=random.randint(30,70), mass=random.randint(1000, 3000))
planet2 = code.objects.Planet((random.randint(200,1000), random.randint(200,1000)), radius=random.randint(30,70), mass=random.randint(1000, 3000))
planet3 = code.objects.Planet((random.randint(200,1000), random.randint(200,1000)), radius=random.randint(30,70), mass=random.randint(1000, 3000))
planet_group = code.objects.Circular_Sprite_Group()
planet_group.add(planet1, planet2, planet3)

golfball = code.objects.Golfball((700,300), planets = planet_group, hit_power=15)
ball_group = code.objects.Circular_Sprite_Group()
ball_group.add(golfball)

while True:
    code.input.update(golfball=golfball)

    screen.fill('black')
    golfball.update()
    planet_group.draw(screen)
    ball_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
