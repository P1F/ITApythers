import pygame
from random import randint
from pygame.locals import *
from game import Point
import menu

get_keys_p1 = True
get_keys_p2 = True


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
        if self.p1.position.x < self.p2.position.x:
            self.p1.facing_left = False
        else:
            self.p1.facing_left = True
        self.p2.facing_left = not self.p1.facing_left

        self.p1.print_me(self.screen)
        self.p2.print_me(self.screen)
        self.clock.print_me(self.screen)

    def mainloop(self):
        background = pygame.image.load('img/Background/' + self.getRandBackground()).convert()
        t0 = pygame.time.get_ticks()
        players = Motion(self.p1, self.p2)

        while True:
            keys = pygame.key.get_pressed()

            if get_keys_p1:
                if not self.p1.jumping:
                    if keys[K_d]:
                        self.p1.right()
                    elif keys[K_a]:
                        self.p1.left()
                    else:
                        self.p1.standing()
                if keys[K_w]:
                    if not self.p1.jumping:
                        self.p1.jumping = True
                        t1 = pygame.time.get_ticks()

            if get_keys_p2:
                if not self.p2.jumping:
                    if keys[K_RIGHT]:
                        self.p2.right()
                    elif keys[K_LEFT]:
                        self.p2.left()
                    else:
                        self.p2.standing()
                if keys[K_UP]:
                    if not self.p2.jumping:
                        self.p2.jumping = True
                        t2 = pygame.time.get_ticks()

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

            players.collide_motion()

            self.clock.update(time - t0)

            self.screen.fill((0, 0, 0))
            # self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)


class Clock:
    def __init__(self):
        self.time_left = 90
        self.has_changed = False
        self.text = menu.Text('90', Point(144, 8))

    def update(self, delta):
        new_time = round(90 - delta / 1000)
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
        self.center_dist = Point(abs(self.hitbox1.center.x - self.hitbox2.center.x),
                                 abs(self.hitbox1.center.y - self.hitbox2.center.y))
        self.width_sum = (self.hitbox1.width + self.hitbox2.width)
        self.height_sum = (self.hitbox1.height + self.hitbox2.height)

    def collide(self):
        x_collide = True if self.center_dist.x <= self.width_sum / 2 else False
        y_collide = True if self.center_dist.y <= self.height_sum / 2 else False

        return x_collide and y_collide

    def penetrate(self):
        x_penetrate = True if self.center_dist.x - self.width_sum / 2 < -1 else False
        y_penetrate = True if self.center_dist.y - self.height_sum / 2 < -1 else False

        return x_penetrate and y_penetrate


class Motion:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.hitboxes = Collision(self.p1.hitbox, self.p2.hitbox)
        self.p1_x0 = None
        self.p2_x0 = None
        self.switching_side = False

    def refresh(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.hitboxes = Collision(self.p1.hitbox, self.p2.hitbox)

    def both_getting_closer(self):
        return (self.p1.going_right and not self.p1.facing_left and self.p2.going_left) or \
               (self.p1.going_left and self.p1.facing_left and self.p2.going_right)

    def some_jumping(self):
        return self.p1.jumping or self.p2.jumping

    def both_jumping(self):
        return self.p1.jumping and self.p2.jumping

    def move_to(self, player, x_position):
        global get_keys_p1
        global get_keys_p2

        if player == self.p1:
            get_keys_p1 = False
        if player == self.p2:
            get_keys_p2 = False

        if player.position.x < x_position - 1.2:
            player.right()
        elif player.position.x > x_position + 1.2:
            player.left()
        else:
            get_keys_p1 = True
            get_keys_p2 = True
            self.switching_side = False

    def switch_side(self):
        if not self.hitboxes.penetrate() and not self.switching_side:
            self.p1_x0 = self.p1.position.x
            self.p2_x0 = self.p2.position.x
            self.switching_side = True
        else:
            self.move_to(self.p1, self.p2_x0)
            self.move_to(self.p2, self.p1_x0)

    def collide_motion(self):
        self.refresh(self.p1, self.p2)
        if self.hitboxes.collide():
            if not self.both_getting_closer() and not self.hitboxes.penetrate():
                if self.p1.going_right and not self.p1.facing_left:
                    self.p2.right()
                if self.p1.going_left and self.p1.facing_left:
                    self.p2.left()
                if self.p2.going_right and not self.p2.facing_left:
                    self.p1.right()
                if self.p2.going_left and self.p2.facing_left:
                    self.p1.left()
            elif (self.both_getting_closer() and not self.some_jumping()) or self.switching_side:
                self.switch_side()
            if self.both_jumping():
                self.p1.going_left = False
                self.p1.going_right = False
                self.p2.going_left = False
                self.p2.going_right = False
