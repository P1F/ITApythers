from game import Point, SpriteSheetLoader
import config
import pygame
from pygame.locals import *

class Fight_stats:
    def __init__(self):
        self.wins_P1 = 0
        self.rounds_P1 = 0
        self.wins_P2 = 0
        self.rounds_P2 = 0
        self.draws = 0
        self.lastwin = 0

    def update(self, tuple):
        rounds_P1, rounds_P2 = tuple[0], tuple[1]
        if rounds_P1 == rounds_P2:
            self.draws += 1
            self.lastwin = 0
        elif rounds_P1 > rounds_P2:
            self.wins_P1 += 1
            self.lastwin = 1
        else:
            self.wins_P2 += 1
            self.lastwin = 2
        self.rounds_P1 += rounds_P1
        self.rounds_P2 += rounds_P2


class Text:
    def __init__(self, string, position):
        self.string = string
        self.position = position
        self.letters = SpriteSheetLoader('img/Ascii.png', 16, 16, True).getSpriteList()
        self.sprite = self.convert()

    def convert(self):
        assert (isinstance(self.string, str))
        length = len(self.string)
        sprite = pygame.Surface((15 * (length + 1), 32)).convert_alpha()
        sprite.fill((0, 0, 0, 0))
        for index in range(length):
            num = ord(self.string[index])
            line = num // 16
            column = num - (line * 16)
            letter = self.letters[line][column]
            if letter != None:
                sprite.blit(letter, (index * 15, 0))
        return sprite

    def print_me(self, screen, position=Point(0, 0)):
        screen.blit(self.sprite, (self.position + position).value())

class Menu:
    def __init__(self, position, screen, screenManager, soundManager, background, cursorpath):
        self.sprites = SpriteSheetLoader('img/Ascii.png', 16, 16).getSpriteList()
        self.screen = screen
        self.screenManager = screenManager
        self.soundManager = soundManager
        self.position = position
        self.background = background
        self.options = []
        self.cursor = pygame.image.load(cursorpath).convert_alpha()

    def back(self):
        return 0

    def mainloop(self):
        background = pygame.image.load('img/Background/' + self.background).convert()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.soundManager.play_sound('menucancel.wav')
                        return self.back()
                    if event.key == K_UP:
                        self.up()
                    if event.key == K_DOWN:
                        self.down()
                    if event.key == K_RIGHT:
                        self.right()
                    if event.key == K_LEFT:
                        self.left()
                    if event.key == K_RETURN:
                        self.enter()

            #self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)


class MenuElt:
    def __init__(self, string, function):
        self.string = string
        self.position = None
        self.text = None
        self.function = function

    def print_me(self, screen):
        self.text.print_me(screen)

    def more(self):
        self.function()

class MainMenu(Menu):
    def __init__(self, screen, screenManager, soundManager, position):
        soundManager.play_music('Intro.mp3')
        Menu.__init__(self, position, screen, screenManager, soundManager, 'MenuScreen.png', 'img/cursor.png')
        self.addElt(MenuElt('Jogar', self.call_game))
        self.addElt(MenuElt('Créditos', self.call_credits))
        self.choice = 0
        self.fight_stats = Fight_stats()

    def addElt(self, elt):
        elt.position = self.position + (15, 3+len(self.options)*16)
        elt.text = Text(elt.string, elt.position)
        self.options.append(elt)

    def call_game(self):
        chars = CharMenu(self.screen, self.screenManager, self.soundManager, 'img/selector.png', Point(100, 200))
        chars.mainloop()

    def call_credits(self):
        print('chamar creditos')

    def print_me(self):
        cursor_pos = self.position + (3, self.choice * 16)
        self.screen.blit(self.cursor, cursor_pos.value())
        for option in self.options:
            option.print_me(self.screen)

    def up(self):
        self.soundManager.play_sound('menumove.wav')
        self.choice -= 1
        if self.choice < 0:
            self.choice = 0

    def down(self):
        self.soundManager.play_sound('menumove.wav')
        self.choice += 1
        if self.choice >= len(self.options):
            self.choice = len(self.options)-1

    def right(self):
        self.soundManager.play_sound('menuok.wav')
        option = self.options[self.choice]
        option.more()

    def left(self):
        self.soundManager.play_sound('menuok.wav')

    def enter(self):
        self.right()


class CharIcon:
    def __init__(self, name, icon, rgb):
        self.name = name
        self.icon = icon
        self.position = None
        self.rgb = rgb

    def print_me(self, screen):
        iconimg = pygame.image.load('img//' + self.icon).convert_alpha()
        iconimg = pygame.transform.scale(iconimg, (16, 16))
        icon = pygame.Surface((16, 16))
        icon.fill(self.rgb)
        icon.blit(iconimg, (0, 0))
        screen.blit(icon, self.position.value())


class CharMenu(Menu):
    def __init__(self, screen, screenManager, soundManager, cursor, position):
        soundManager.play_music('char.mp3')
        Menu.__init__(self, position, screen, screenManager, soundManager, 'charselect.png', cursor)
        self.addChar(CharIcon('Pelá', 'pela.png', (0, 100, 0)))

    def addChar(self, charicon):
        charicon.position = self.position
        self.options.append(charicon)

    def print_me(self):
        for charicon in self.options:
            charicon.print_me(self.screen)