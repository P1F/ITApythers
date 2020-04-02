import pygame
from random import randint
from pygame.locals import *
from game import Point


class FightManager():
    def __init__(self, p1, p2, screen, screenManager, soundManager):
        self.p1 = p1
        p1.load(Point(0, 140))
        self.p2 = p2
        p2.load(Point(200, 140))
        self.screen = screen
        self.screenManager = screenManager
        self.soundManager = soundManager

    def getRandBackground(self):
        return str(randint(1, 4)) + '.png'

    def print_me(self):
        self.p1.print_me(self.screen)
        self.p2.print_me(self.screen)

    def mainloop(self):
        background = pygame.image.load('img/Background/' + self.getRandBackground()).convert()
        while True:
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT]:
                self.p2.right()
            if keys[K_LEFT]:
                self.p2.left()
            if keys[K_d]:
                self.p1.right()
            if keys[K_a]:
                self.p1.left()
            if keys[K_UP]:
                if not self.p2.jumping:
                    self.p2.jumping = True
                    t2 = pygame.time.get_ticks()
            if keys[K_w]:
                if not self.p1.jumping:
                    self.p1.jumping = True
                    t1 = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.soundManager.play_sound('menucancel.wav')
                        return 0
                elif event.type == QUIT:
                    exit()

            if self.p1.jumping:
                self.p1.jump(pygame.time.get_ticks() - t1)
            if self.p2.jumping:
                self.p2.jump(pygame.time.get_ticks() - t2)

            self.screen.fill((0, 0, 0))
            #self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)