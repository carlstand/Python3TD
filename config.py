import pygame

pygame.init()
screen_info = pygame.display.Info()
print(screen_info)

SCREEN_SIZE = (int(screen_info.current_w/2), int(screen_info.current_h/2))
print(SCREEN_SIZE)