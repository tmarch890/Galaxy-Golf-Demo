import pygame
from sys import exit

# def a


def update(**kwargs):
    inputs = pygame.event.get()
    for event in inputs:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 'golfball' in kwargs:
                kwargs['golfball'].launching = True

        if event.type == pygame.MOUSEBUTTONUP:
            if 'golfball' in kwargs:
                kwargs['golfball'].launch()
                kwargs['golfball'].launching = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if 'golfball' in kwargs:
                    kwargs['golfball'].reset_ball()
