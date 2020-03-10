import pygame
class Char:
    def __init__(self, name, rgb, index):
        self.name = name
        self.position = None
        self.rgb = rgb
        self.index = index

    def print_icon(self, screen):
        iconimg = pygame.image.load('personagens//' + str(self.index) + '//icon.png').convert_alpha()
        iconimg = pygame.transform.scale(iconimg, (32, 24))
        icon = pygame.Surface((32, 24))
        icon.fill(self.rgb)
        icon.blit(iconimg, (0, 0))
        screen.blit(icon, self.position.value())

    def print_selected(self, screen, position):
        iconimg = pygame.image.load('personagens//' + str(self.index) + '//icon.png').convert_alpha()
        iconimg = pygame.transform.scale(iconimg, (98, 98))
        screen.blit(iconimg, position.value())