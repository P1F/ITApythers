import pygame


class Char:
    def __init__(self, name, rgb, index):
        self.icon = CharIcon(rgb, index)
        self.name = name
        self.position = None
        self.rgb = rgb
        self.index = index

    def print_me(self):
        print('char')


class CharIcon:
    def __init__(self, rgb, index):
        self.rgb = rgb
        self.index = index
        self.position = None

    def print_me(self, screen):
        iconimg = pygame.image.load('personagens//' + str(self.index) + '//icon.png').convert_alpha()
        iconimg = pygame.transform.scale(iconimg, (32, 24))
        icon = pygame.Surface((32, 24))
        icon.fill(self.rgb)
        icon.blit(iconimg, (0, 0))
        screen.blit(icon, self.position.value())


