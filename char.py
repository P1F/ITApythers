import pygame
from game import SpriteSheetLoader, Point


class Char:
    def __init__(self, name, rgb, index):
        self.icon = CharIcon(rgb, index)
        self.name = name
        self.index = index
        self.position = None
        self.height = None
        self.sprites = None
        self.spriteline = 0
        self.spritecolumn = 0
        self.jumping = False

    def load(self, start_position):
        self.sprites = SpriteSheetLoader('personagens//' + str(self.index) + '//sprites.png', 120, 100).getSpriteList()
        self.position = start_position
        self.height = start_position.y

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


