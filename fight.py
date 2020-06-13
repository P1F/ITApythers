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
            if not self.p1.jumping:
                self.p1.velocity = 0
                if keys[K_d]:
                    self.p1.right(self.p2.hitbox)
                if keys[K_a]:
                    self.p1.left(self.p2.hitbox)
            if keys[K_w]:
                if not self.p1.jumping:
                    self.p1.jumping = True
                    t1jump = pygame.time.get_ticks()
            if keys[K_e]:
                if not self.p1.punch_animation:
                    self.p1.punching = self.p1.punch_animation = True
                    t1punch = pygame.time.get_ticks()
            if keys[K_r]:
                if not self.p1.kick_animation:
                    self.p1.kicking = self.p1.kick_animation = True
                    t1kick = pygame.time.get_ticks()
            if keys[K_t]:
                if not self.p1.superpower.active:
                    self.p1.launch_superpower(self.p2)

            if not self.p2.jumping:
                self.p2.velocity = 0
                if keys[K_RIGHT]:
                    self.p2.right(self.p1.hitbox)
                if keys[K_LEFT]:
                    self.p2.left(self.p1.hitbox)
            if keys[K_UP]:
                if not self.p2.jumping:
                    self.p2.jumping = True
                    t2jump = pygame.time.get_ticks()
            if keys[K_j]:
                if not self.p2.punch_animation:
                    self.p2.punching = self.p2.punch_animation = True
                    t2punch = pygame.time.get_ticks()
            if keys[K_k]:
                if not self.p2.kick_animation:
                    self.p2.kicking = self.p2.kick_animation = True
                    t2kick = pygame.time.get_ticks()
            if keys[K_l]:
                if not self.p2.superpower.active:
                    self.p2.launch_superpower(self.p1)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.soundManager.play_sound('menucancel.wav')
                        return 0
                elif event.type == QUIT:
                    exit()

            time = pygame.time.get_ticks()

            if self.p1.jumping:
                self.p1.jump(time - t1jump, self.p2.hitbox)
            if self.p1.punch_animation:
                self.p1.punch(time - t1punch, self.p2)
            if self.p1.kick_animation:
                self.p1.kick(time - t1kick, self.p2)
            if self.p1.superpower.active:
                self.p1.superpower.launch(self.p1, self.p2, 20)
            if self.p2.jumping:
                self.p2.jump(time - t2jump, self.p1.hitbox)
            if self.p2.punch_animation:
                self.p2.punch(time - t2punch, self.p1)
            if self.p2.kick_animation:
                self.p2.kick(time - t2kick, self.p1)
            if self.p2.superpower.active:
                self.p2.superpower.launch(self.p2, self.p1, 20)

            self.clock.update(time - t0)

            self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)


class Clock:
    def __init__(self):
        self.time_left = 90
        self.has_changed = True
        self.text = menu.Text('', Point(144, 8))

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
