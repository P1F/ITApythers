import pygame
from game import SpriteSheetLoader, Point


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class HitBox:
    def __init__(self, position, color, width, height):
        self.position = position
        self.color = color
        self.width = width
        self.height = height

    def refresh(self, player):
        if player.jumping:
            self.width = 29
            self.height = 50
            self.position = player.position + (50, 50)
        else:
            self.width = 29
            self.height = 40
            self.position = player.position + (45, 60)


    def draw(self, player, screen):
        self.refresh(player)
        pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, self.width, self.height), 1)


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

        self.hitbox = None

    def load(self, player_one):
        self.sprites = SpriteSheetLoader('personagens//' + str(self.index) + '//sprites.png', 120, 100).getSpriteList()
        if player_one:
            self.position = Point(0, 140)
            color = red
        else:
            self.position = Point(200, 140)
            color = green
        self.height = self.position.y
        self.health = HealthBar(player_one)
        self.hitbox = HitBox(self.position, color, 29, 40)

    def right(self):
        if not self.jumping:
            if self.spriteline != 1:
                self.spriteline = 1
                self.spritecolumn = 0
            else:
                self.spritecolumn += 1
                if self.spritecolumn > 239:
                    self.spritecolumn = 0

        new = self.position + (0.2, 0)
        if new.x < 240:
            self.position = new

    def left(self):
        if not self.jumping:
            if self.spriteline != 1:
                self.spriteline = 1
                self.spritecolumn = 0
            else:
                self.spritecolumn += 1
                if self.spritecolumn > 239:
                    self.spritecolumn = 0

        new = self.position - (0.2, 0)
        if new.x > -40:
            self.position = new

    def standing(self):
        if not self.jumping:
            if self.spriteline != 0:
                self.spriteline = 0
                self.spritecolumn = 0
            else:
                self.spritecolumn += 1
                if self.spritecolumn > 239:
                    self.spritecolumn = 0

    def jump(self, delta):
        if not 6 <= self.spriteline <= 7:
            self.spriteline = 7
            self.spritecolumn = 0

        deltah = 0.32 * delta - 0.0004 * delta * delta
        if deltah < 0:
            self.jumping = False
            self.position.y = self.height
            self.spritecolumn = 0
            self.spriteline = 0
            return

        last_pos = self.position.y
        self.position.y = self.height - deltah
        dy_dt = abs(self.position.y - last_pos)

        if self.spriteline == 7 and self.position.y != last_pos and dy_dt < 10 ** -2:
            self.spriteline = 6

    def print_me(self, screen):
        screen.blit(self.sprites[self.spriteline][self.spritecolumn//60], self.position.value())
        self.health.print_me(screen)
        self.hitbox.draw(self, screen)


class CharIcon:
    def __init__(self, rgb, index):
        self.rgb = rgb
        self.position = None
        self.iconimg = pygame.transform.scale(
            pygame.image.load('personagens//' + str(index) + '//icon.png').convert_alpha(), (32, 24))

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
            return 143 - health_bar_width, 10
        else:
            return 177, 10

    def print_me(self, screen):
        health_bar_width = int(140 * self.health / 100)
        img = pygame.transform.scale(self.img, (health_bar_width, 12))
        screen.blit(img, self.get_position(self.player_one, health_bar_width))