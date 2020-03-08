import config
import pygame
import menu
from game import Point
import time

if __name__ == '__main__':
    print('carregando...')

    pygame.init()
    pygame.mixer.init()

    screenManager = config.Screen()
    soundManager = config.SoundPlayer()

    screen = pygame.Surface((640, 480), 0, 32)
    menu = menu.MainMenu(screen, screenManager, soundManager, Point(80, 150))
    menu.mainloop()