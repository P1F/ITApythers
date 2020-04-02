import pygame
from game import SpriteSheetLoader, Point


class Char:
    def __init__(self, name, rgb, index):
        self.icon = CharIcon(rgb, index)
        self.health = None
        self.name = name
        self.index = index

        self.position = None
        self.height = None

        self.sprites = None
        self.spriteline = 0
        self.spritecolumn = 0

        self.jumping = False

    def load(self, player_one):
        self.sprites = SpriteSheetLoader('personagens//' + str(self.index) + '//sprites.png', 120, 100).getSpriteList()
        if player_one:
            self.position = Point(0, 140)
        else:
            self.position = Point(200, 140)
        self.height = self.position.y
        self.health = HealthBar(player_one)

    def right(self):
        new = self.position + (0.2, 0)
        if new.x < 240:
            self.position = new

    def left(self):
        new = self.position - (0.2, 0)
        if new.x > -40:
            self.position = new

    def jump(self, delta):
        deltah = 0.32*delta - 0.0004*delta*delta
        if deltah < 0:
            self.jumping = False
            self.position.y = self.height
            return
        self.position.y = self.height - deltah

    def print_me(self, screen):
        screen.blit(self.sprites[self.spriteline][self.spritecolumn], self.position.value())
        self.health.print_me(screen)


class CharIcon:
    def __init__(self, rgb, index):
        self.rgb = rgb
        self.position = None
        self.iconimg = pygame.transform.scale(pygame.image.load('personagens//' + str(index) + '//icon.png').convert_alpha(), (32, 24))

    def print_me(self, screen):
        icon = pygame.Surface((32, 24))
        icon.fill(self.rgb)
        icon.blit(self.iconimg, (0, 0))
        screen.blit(icon, self.position.value())


class HealthBar:
    def __init__(self, player_one):
        self.health = 100
        self.img = pygame.image.load('img//healthbar.png').convert_alpha()
        self.player_one = player_one

    def get_position(self, player_one, health_bar_width):
        if player_one:
            return 143-health_bar_width, 10
        else:
            return 177, 10

    def print_me(self, screen):
        health_bar_width = int(140*self.health/100)
        img = pygame.transform.scale(self.img, (health_bar_width, 12))
        screen.blit(img, self.get_position(self.player_one, health_bar_width))

