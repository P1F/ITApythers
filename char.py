import pygame
from game import SpriteSheetLoader, Point


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
        self.punching = self.punch_animation = False

        self.sprites = self.spriteline = self.spritecolumn = self.hitbox = self.health = None

    def load(self, is_left_player):
        self.sprites = SpriteSheetLoader('personagens//' + str(self.index) + '//sprites.png', 120, 100).getSpriteList()
        self.spriteline = 0
        self.spritecolumn = 0
        if is_left_player:
            self.hitbox = Hitbox(30, 40, Point(45, 200), True)
        else:
            self.hitbox = Hitbox(30, 40, Point(245, 200), False)
        self.health = HealthBar(is_left_player)

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
            self.hitbox.update_side(other)
            if collide(self.hitbox, other):
                if self.hitbox.is_left_player:
                    self.hitbox.x = other.x - other.width - 1
                else:
                    self.hitbox.x = other.x + other.width + 1
            return
        self.hitbox.y = self.hitbox.ground - deltah

    def punch(self, delta, other):
        self.spriteline = 21
        if delta > 150 and self.punching:
            self.spritecolumn = 1
            if self.hitbox.is_left_player:
                hitbox = Hitbox(18, 30, Point(self.hitbox.x + self.hitbox.width, self.hitbox.y))
            else:
                hitbox = Hitbox(18, 30, Point(self.hitbox.x - 18, self.hitbox.y))
            if collide(hitbox, other.hitbox):
                other.health.take_damage(10)
            self.punching = False
        elif delta>250:
            self.spriteline = self.spritecolumn = 0
            self.punch_animation = False

    def print_me(self, screen):
        sprite = self.sprites[self.spriteline][self.spritecolumn]
        if not self.hitbox.is_left_player:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, self.hitbox.get_print_pos())
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
    def __init__(self, is_left_player):
        self.value = 100
        self.img = pygame.image.load('img//healthbar.png').convert_alpha()
        self.redbar = pygame.image.load('img//redbar.png').convert_alpha()
        self.damage = 0
        self.is_left_player = is_left_player

    def get_health_bar_position(self, is_left_player, health_bar_width):
        if is_left_player:
            return 143-health_bar_width, 10
        else:
            return 177, 10

    def get_red_bar_position(self, is_left_player, health_bar_position, health_bar_width, red_bar_width):
        if is_left_player:
            return health_bar_position[0] - red_bar_width, health_bar_position[1]
        else:
            return health_bar_position[0] + health_bar_width - 1, health_bar_position[1]

    def take_damage(self, dmg):
        self.value -= dmg
        self.damage += dmg

    def print_me(self, screen):
        health_bar_width = int(140 * self.value / 100)
        health_bar_position = self.get_health_bar_position(self.is_left_player, health_bar_width)
        if self.damage > 0:
            red_bar_width = int(140 * self.damage / 100) + 1
            red_bar = pygame.transform.scale(self.redbar, (red_bar_width, 10))
            screen.blit(red_bar, self.get_red_bar_position(self.is_left_player, health_bar_position, health_bar_width, red_bar_width))
            self.damage -= 0.01

        health_bar_width = int(140 * self.value / 100)
        health_bar = pygame.transform.scale(self.img, (health_bar_width, 12))
        screen.blit(health_bar, health_bar_position)


class Hitbox:
    def __init__(self, width, height, position, is_left_player = None):
        self.width = width
        self.height = height
        self.is_left_player = is_left_player
        #coordinates for the upper left point of the hitbox
        self.x = position.x
        self.y = self.ground = position.y

    def get_print_pos(self):
        return self.x - 45, self.y - 60

    def update_side(self, other):
        if self.x < other.x:
            self.is_left_player = True
            other.is_left_player = False
        else:
            self.is_left_player = False
            other.is_left_player = True

