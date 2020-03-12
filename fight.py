import pygame
from random import randint


class FightManager():
    def __init__(self, p1, p2, screen, screenManager, soundManager):
        self.p1 = p1
        self.p2 = p2
        self.screen = screen
        self.screenManager = screenManager
        self.soundManager = soundManager

    def getRandBackground(self):
        return str(randint(0, 4)) + '.png'

    def print_me(self):
        self.p1.print_me()
        self.p2.print_me()

    def mainloop(self):
        background = pygame.image.load('img/Background/' + self.getRandBackground()).convert()
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)