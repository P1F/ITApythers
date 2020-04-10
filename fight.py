import pygame
from random import randint
from pygame.locals import *
from game import Point
import menu


class FightManager:
    def __init__(self, p1, p2, screen, screenManager, soundManager):
        self.p1 = p1
        p1.load(True)
        self.p2 = p2
        p2.load(False)
        self.clock = Clock()
        self.screen = screen
        self.screenManager = screenManager
        self.soundManager = soundManager

    def getRandBackground(self):
        return str(randint(1, 4)) + '.png'

    def print_me(self):
        self.p1.print_me(self.screen)
        self.p2.print_me(self.screen)
        self.clock.print_me(self.screen)

    def mainloop(self):
        background = pygame.image.load('img/Background/' + self.getRandBackground()).convert()
        t0 = pygame.time.get_ticks()

        while True:
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.p2.right()
            elif keys[K_LEFT]:
                self.p2.left()
            else:
                self.p2.standing()

            if keys[K_d]:
                self.p1.right()
            elif keys[K_a]:
                self.p1.left()
            else:
                self.p1.standing()

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

            time = pygame.time.get_ticks()

            if self.p1.jumping:
                self.p1.jump(time - t1)
            if self.p2.jumping:
                self.p2.jump(time - t2)

            self.clock.update(time - t0)

            self.screen.fill((0, 0, 0))
            #self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)


class Clock:
    def __init__(self):
        self.time_left = 90
        self.has_changed = False
        self.text = menu.Text('90', Point(144, 8))

    def update(self, delta):
        new_time = round(90 - delta/1000)
        if new_time != self.time_left:
            self.time_left = new_time
            self.has_changed = True

    def print_me(self, screen):
        brdr = pygame.Surface((32, 24), 0, 32)
        brdr.fill((255, 0, 0))
        sqr = pygame.Surface((30, 22), 0, 32)
        sqr.fill((0, 255, 0))
        brdr.blit(sqr, (1, 1))
        screen.blit(brdr, (144, 4))

        if self.has_changed:
            self.text.string = str(self.time_left)
            self.text.sprite = self.text.convert()
            self.has_changed = False
        self.text.print_me(screen)


class Collision:
    def __init__(self, hitbox1, hitbox2):
        self.hitbox1 = hitbox1
        self.hitbox2 = hitbox2

    def collide(self):
        center1 = Point(self.hitbox1.position.x + self.hitbox1.width/2, self.hitbox1.position.y + self.hitbox1.height/2)
        center2 = Point(self.hitbox2.position.x + self.hitbox2.width/2, self.hitbox2.position.y + self.hitbox2.height/2)
        x_collide = True if abs(center1.x - center2.x) <= (self.hitbox1.width + self.hitbox2.width)/2 else False
        y_collide = True if abs(center1.y - center2.y) <= (self.hitbox1.height + self.hitbox2.height)/2 else False

        return x_collide and y_collide