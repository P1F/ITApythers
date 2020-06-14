import pygame
from game import SpriteSheetLoader, Point

# STATES
# IDLE -> 0
# WALKING LEFT  -> 1
# WALKING RIGHT -> 2
# JUMPING -> 3


# checks if lines x and y collide, with y >= x

def one_dimension_collide(x0, x1, y0, y1):
    return (y0 <= x0 <= y1) or (y0 <= x1 <= y1)


def collide(p1, p2):
    if p1.width <= p2.width and p1.height <= p2.height:
        return one_dimension_collide(p1.x, p1.x + p1.width, p2.x, p2.x + p2.width) and \
               one_dimension_collide(p1.y, p1.y + p1.height, p2.y, p2.y + p2.height)
    elif p1.width <= p2.width and p1.height > p2.height:
        return one_dimension_collide(p1.x, p1.x + p1.width, p2.x, p2.x + p2.width) and \
               one_dimension_collide(p2.y, p2.y + p2.height, p1.y, p1.y + p1.height)
    elif p1.width > p2.width and p1.height <= p2.height:
        return one_dimension_collide(p2.x, p2.x + p2.width, p1.x, p1.x + p1.width) and \
               one_dimension_collide(p1.y, p1.y + p1.height, p2.y, p2.y + p2.height)
    else:
        return one_dimension_collide(p2.x, p2.x + p2.width, p1.x, p1.x + p1.width) and \
               one_dimension_collide(p2.y, p2.y + p2.height, p1.y, p1.y + p1.height)


class Char:
    def __init__(self, name, rgb, index):
        self.icon = CharIcon(rgb, index)
        self.name = name
        self.index = index
        self.velocity = None

        self.jumping = False
        self.going_left = self.going_right = self.going_up = self.going_down = False
        self.punching = self.punch_animation = False
        self.kicking = self.kick_animation = False

        self.last_state = self.actual_state = None
        self.sprites = self.spriteline = self.spritecolumn = None
        self.hitbox = self.health = self.power_bar = self.superpower = None

    def load(self, is_left_player):
        self.sprites = SpriteSheetLoader('personagens//' + str(self.index) + '//sprites.png', 120, 100).getSpriteList()
        self.spriteline = 0
        self.spritecolumn = 0
        self.last_state = self.actual_state = 0
        if is_left_player:
            self.hitbox = Hitbox(30, 40, Point(45, 200), True)
        else:
            self.hitbox = Hitbox(30, 40, Point(245, 200), False)
        self.health = HealthBar(is_left_player)
        self.power_bar = PowerBar(is_left_player)
        self.superpower = SuperPower(self.index)
        self.superpower.load(is_left_player)

    def set_state(self, state):
        if state == 0:  # idle
            self.jumping = self.going_left = self.going_right = self.going_up = self.going_down = False
        elif state == 1:  # left
            self.going_left = True
            self.jumping = self.going_right = self.going_up = self.going_down = False
        elif state == 2:  # right
            self.going_right = True
            self.jumping = self.going_left = self.going_up = self.going_down = False
        elif state == 3:  # jumping
            self.jumping = True
            self.going_left = self.going_right = self.going_up = self.going_down = False
        if self.actual_state == 3:
            self.last_state = self.actual_state
        if self.last_state == state:
            return
        self.last_state = self.actual_state
        self.actual_state = state

    def right(self, other):
        self.velocity = 0.2
        self.hitbox.x += self.velocity
        if self.hitbox.x + self.hitbox.width > 320 or collide(self.hitbox, other):
            self.hitbox.x -= self.velocity

    def left(self, other):
        self.velocity = -0.2
        self.hitbox.x += self.velocity
        if self.hitbox.x < 0 or collide(self.hitbox, other):
            self.hitbox.x -= self.velocity

    def jump(self, delta, other):
        deltah = 0.40 * delta - 0.0004 * delta * delta
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
        self.going_up = True
        if self.hitbox.y < 102:
            self.going_down = True
        if self.velocity != 0 and (self.hitbox.x + self.hitbox.width <= 320) and self.hitbox.x >= 0:
            self.hitbox.x += self.velocity

    def punch(self, delta, other):
        dmg = 5
        if not self.jumping:
            self.spriteline = 21
        else:
            self.spriteline = 25
        if delta > 150 and self.punching:
            self.spritecolumn = 1
            if self.hitbox.is_left_player:
                hitbox = Hitbox(18, 30, Point(self.hitbox.x + self.hitbox.width, self.hitbox.y))
            else:
                hitbox = Hitbox(18, 30, Point(self.hitbox.x - 18, self.hitbox.y))
            if collide(hitbox, other.hitbox):
                other.take_hit(dmg)
                self.power_bar.up(dmg, False)
            self.punching = False
        elif delta > 250:
            self.spriteline = self.spritecolumn = 0
            other.spriteline = other.spritecolumn = 0
            self.punch_animation = False

    def kick(self, delta, other):
        dmg = 5
        if not self.jumping:
            self.spriteline = 23
        else:
            self.spriteline = 28
        if delta > 150 and self.kicking:
            self.spritecolumn = 1
            if self.hitbox.is_left_player:
                hitbox = Hitbox(18, 30, Point(self.hitbox.x + self.hitbox.width, self.hitbox.y))
            else:
                hitbox = Hitbox(18, 30, Point(self.hitbox.x - 18, self.hitbox.y))
            if collide(hitbox, other.hitbox):
                other.take_hit(dmg)
                self.power_bar.up(dmg, False)
            self.kicking = False
        elif delta > 250:
            self.spriteline = self.spritecolumn = 0
            other.spriteline = other.spritecolumn = 0
            self.kick_animation = False

    def launch_superpower(self, other):
        if self.power_bar.is_ready():
            self.superpower.active = True
            self.superpower.hitbox.x = self.hitbox.x
            self.superpower.hitbox.y = self.hitbox.y
            self.power_bar.value = 0
            self.spritecolumn = 1
            self.spriteline = 33

    def take_hit(self, dmg):
        self.health.take_damage(dmg)
        self.power_bar.up(dmg, True)
        self.spritecolumn = 0
        if not self.jumping:
            self.spriteline = 9
        else:
            self.spriteline = 19

    def set_anim(self, time):
        # not considering combat moves
        if self.last_state == self.actual_state:
            if time > 100:
                line_len = len(self.sprites[self.spriteline])
                self.spritecolumn += 1
                self.spritecolumn %= line_len
            return
        self.spritecolumn = 0
        if self.actual_state == 0:  # idle
            self.spriteline = 0
        if self.actual_state == 1 or self.actual_state == 2:  # walking
            self.spriteline = 1
        if self.actual_state == 3:  # jumping
            if self.going_up and not self.going_down:
                self.spriteline = 6
            elif self.going_down:
                self.spriteline = 7

    def print_me(self, screen):
        sprite = self.sprites[self.spriteline][self.spritecolumn]
        if not self.hitbox.is_left_player:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, self.hitbox.get_print_pos(True))
        self.health.print_me(screen)
        self.power_bar.print_me(screen)
        if self.superpower.active:
            self.superpower.print_me(screen)


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
    def __init__(self, is_left_player):
        self.value = 100
        self.img = pygame.image.load('img//healthbar.png').convert_alpha()
        self.redbar = pygame.image.load('img//redbar.png').convert_alpha()
        self.damage = 0
        self.is_left_player = is_left_player

    def get_health_bar_position(self, is_left_player, health_bar_width):
        if is_left_player:
            return 143 - health_bar_width, 10
        else:
            return 177, 10

    def get_red_bar_position(self, is_left_player, health_bar_position, health_bar_width, red_bar_width):
        if is_left_player:
            return health_bar_position[0] - red_bar_width, health_bar_position[1]
        else:
            return health_bar_position[0] + health_bar_width - 1, health_bar_position[1]

    def take_damage(self, dmg):
        if self.value > 0:
            self.value -= dmg
            self.damage += dmg

    def print_me(self, screen):
        health_bar_width = int(140 * self.value / 100)
        health_bar_position = self.get_health_bar_position(self.is_left_player, health_bar_width)
        if self.damage > 0:
            red_bar_width = int(140 * self.damage / 100) + 1
            red_bar = pygame.transform.scale(self.redbar, (red_bar_width, 10))
            screen.blit(red_bar, self.get_red_bar_position(
                self.is_left_player, health_bar_position, health_bar_width, red_bar_width))
            self.damage -= 0.01

        health_bar_width = int(140 * self.value / 100)
        health_bar = pygame.transform.scale(self.img, (health_bar_width, 12))
        screen.blit(health_bar, health_bar_position)


class PowerBar:
    def __init__(self, is_left_player):
        self.value = 0
        self.img = pygame.image.load('img//powerbar.png').convert_alpha()
        self.is_left_player = is_left_player

    def get_power_bar_position(self, is_left_player, power_bar_width):
        if is_left_player:
            return 143 - power_bar_width, 30
        else:
            return 177, 30

    def up(self, dmg, hit_taken):
        if self.value < 100:
            if hit_taken:
                self.value += dmg * 2
            else:
                self.value += dmg * 4
        elif self.value > 100:
            self.value = 100

    def print_me(self, screen):
        power_bar_width = int(140 * self.value / 100)
        power_bar_position = self.get_power_bar_position(self.is_left_player, power_bar_width)
        power_bar_width = int(140 * self.value / 100)
        power_bar = pygame.transform.scale(self.img, (power_bar_width, 12))
        screen.blit(power_bar, power_bar_position)

    def is_ready(self):
        if self.value == 100:
            return True
        return False


class Hitbox:
    def __init__(self, width, height, position, is_left_player=None):
        self.width = width
        self.height = height
        self.is_left_player = is_left_player
        # coordinates for the upper left point of the hitbox
        self.x = position.x
        self.y = self.ground = position.y

    def get_print_pos(self, is_player):
        if is_player:
            return self.x - 45, self.y - 60
        else:  # is superpower
            if self.is_left_player:
                return self.x - 5, self.y - 28
            else:
                return self.x - 25, self.y - 28

    def update_side(self, other):
        if self.x < other.x:
            self.is_left_player = True
            other.is_left_player = False
        else:
            self.is_left_player = False
            other.is_left_player = True

    # retirar no final do jogo
    def print_me(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), rect, 1)


class SuperPower:
    def __init__(self, player_idx):
        self.sprites = self.spriteline = self.spritecolumn = self.hitbox = None
        self.player_idx = player_idx
        self.active = False

    def load(self, is_left_player):
        self.sprites = SpriteSheetLoader('img//superpower.png', 60, 60).getSpriteList()
        self.spriteline = 0
        self.spritecolumn = 0
        if is_left_player:
            self.hitbox = Hitbox(30, 25, Point(45, 180), True)
        else:
            self.hitbox = Hitbox(30, 25, Point(245, 180), False)

    def launch(self, player, other, dmg):
        if not collide(self.hitbox, other.hitbox) and -self.hitbox.width <= self.hitbox.x <= 320:
            if player.hitbox.is_left_player:
                self.hitbox.x += 0.4
            else:
                self.hitbox.x -= 0.4
        elif collide(self.hitbox, other.hitbox):
            other.take_hit(dmg)
            player.power_bar.value += dmg*4
            self.active = False
        else:
            self.active = False

    def print_me(self, screen):
        sprite = self.sprites[self.spriteline][self.spritecolumn]
        if not self.hitbox.is_left_player:
            sprite = pygame.transform.flip(sprite, True, False)
        screen.blit(sprite, self.hitbox.get_print_pos(False))
