import pygame
import random
import os

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue



    screen.fill((0, 0, 0))
    if is_blue:
        color = (0, 128, 255)
    else:
        color = (0, 100, 0)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    pygame.display.flip()
    clock.tick(60)

quit()
