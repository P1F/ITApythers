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

    screen = pygame.Surface((320, 240), 0, 32)
    menu = menu.MainMenu(screen, screenManager, soundManager, Point(90, 160), 'MenuScreen.png')
    menu.mainloop()