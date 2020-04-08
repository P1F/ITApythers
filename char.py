import pygame
from game import SpriteSheetLoader


#checks if lines x and y collide, with y >= x
def one_dimension_collide(x0, x1, y0, y1):
    return (x0 >= y0 and x0 <= y1) or (x1>= y0 and x1 <= y1)


def collide(p1, p2):
    if p1.width <= p2.width and p1.height <= p2.height:
        return one_dimension_collide(p1.x, p1.x + p1.width, p2.x, p2.x + p2.width) and one_dimension_collide(p1.y, p1.y + p1.height, p2.y, p2.y + p2.height)
    elif p1.width <= p2.width and p1.height > p2.height:
        return one_dimension_collide(p1.x, p1.x + p1.width, p2.x, p2.x + p2.width) and one_dimension_collide(p2.y, p2.y + p2.height, p1.y, p1.y + p1.height)
    elif p1.width > p2.width and p1.height <= p2.height:
        return one_dimension_collide(p2.x, p2.x + p2.width, p1.x, p1.x + p1.width) and one_dimension_collide(p1.y, p1.y + p1.height, p2.y, p2.y + p2.height)
    else:
        return one_dimension_collide(p2.x, p2.x + p2.width, p1.x, p1.x + p1.width) and one_dimension_collide(p2.y, p2.y + p2.height, p1.y, p1.y + p1.height)


class Char:
    def __init__(self, name, rgb, index):
        self.icon = CharIcon(rgb, index)
        self.name = name
        self.index = index

        self.jumping = False

    def load(self, player_one):
        self.sprites = SpriteSheetLoader('personagens//' + str(self.index) + '//sprites.png', 120, 100).getSpriteList()
        self.spriteline = 0
        self.spritecolumn = 0
        self.hitbox = Hitbox(30, 40, player_one)
        self.health = HealthBar(player_one)

    def right(self, other):
        self.hitbox.x += 0.2
        if self.hitbox.x + self.hitbox.width > 320 or collide(self.hitbox, other):
            self.hitbox.x -= 0.2

    def left(self, other):
        self.hitbox.x -= 0.2
        if self.hitbox.x < 0 or collide(self.hitbox, other):
            self.hitbox.x += 0.2

    def jump(self, delta, other):
        deltah = 0.40*delta - 0.0004*delta*delta
        if deltah < 0:
            self.jumping = False
            self.hitbox.y = self.hitbox.ground
            if collide(self.hitbox, other):
                if self.hitbox.x > other.x:
                    self.hitbox.x = other.x + other.width + 1
                else:
                    self.hitbox.x = other.x - other.width - 1
            return
        self.hitbox.y = self.hitbox.ground - deltah

    def print_me(self, screen):
        screen.blit(self.sprites[self.spriteline][self.spritecolumn], self.hitbox.get_print_pos())
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
        self.value = 100
        self.img = pygame.image.load('img//healthbar.png').convert_alpha()
        self.player_one = player_one

    def get_position(self, player_one, health_bar_width):
        if player_one:
            return 143-health_bar_width, 10
        else:
            return 177, 10

    def print_me(self, screen):
        health_bar_width = int(140*self.value/100)
        img = pygame.transform.scale(self.img, (health_bar_width, 12))
        screen.blit(img, self.get_position(self.player_one, health_bar_width))


class Hitbox:
    def __init__(self, width, height, player_one):
        self.width = width
        self.height = height
        self.ground = 200
        #coordinates for the upper left point of the hitbox
        if player_one:
            self.x = 45
        else:
            self.x = 245
        self.y = 200

    def get_print_pos(self):
        return self.x - 45, self.y - 60

