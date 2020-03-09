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
    def __init__(self, position, screen, screenManager, soundManager, cursor):
        self.sprites = SpriteSheetLoader('img/Ascii.png', 16, 16).getSpriteList()
        self.screen = screen
        self.screenManager = screenManager
        self.soundManager = soundManager
        self.position = position
        self.options = []
        self.cursor = pygame.image.load(cursor).convert_alpha()
        self.choice = 0

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

            self.screen.fill((0, 0, 0))
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
    def __init__(self, screen, screenManager, soundManager, position, background):
        soundManager.play_music('Intro.mp3')
        Menu.__init__(self, position, screen, screenManager, soundManager, 'img/cursor.png')
        self.background = background
        self.addElt(MenuElt('Jogar', self.call_game))
        self.addElt(MenuElt('Créditos', self.call_credits))
        self.fight_stats = Fight_stats()

    def addElt(self, elt):
        elt.position = self.position + (15, 3+len(self.options)*16)
        elt.text = Text(elt.string, elt.position)
        self.options.append(elt)

    def call_game(self):
        chars = CharSelector(self.screen, self.screenManager, self.soundManager, 'img/selector.png', 'charselect.png')
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
    def __init__(self, name, rgb, index):
        self.name = name
        self.position = None
        self.rgb = rgb
        self.index = index

    def print_me(self, screen):
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


class CharMenu(Menu):
    def __init__(self, screen, screenManager, soundManager, cursor, position, selectedposition):
        soundManager.play_music('char.mp3')
        Menu.__init__(self, position, screen, screenManager, soundManager, cursor)
        self.selectedposition = selectedposition
        self.selected = False
        self.cursorpath = cursor
        self.addChar(CharIcon('Pelá', (0, 100, 0), 1))
        self.addChar(CharIcon('José', (0, 0, 100), 2))
        self.addChar(CharIcon('Mario', (100, 0, 0), 3))
        self.addChar(CharIcon('Luigi', (100, 100, 100), 4))

    def addChar(self, charicon):
        charicon.position = self.position + ((len(self.options)%2)*32, int(len(self.options)/2)*24)
        self.options.append(charicon)

    def print_me(self):
        for charicon in self.options:
            charicon.print_me(self.screen)

        self.options[self.choice].print_selected(self.screen, self.selectedposition)

        if self.cursor is not None:
            cursor_pos = self.position - (3, 2) + ((self.choice%2)*32, (int(self.choice/2))*24)
            self.cursor = pygame.transform.scale(self.cursor, (36, 27))
            self.screen.blit(self.cursor, cursor_pos.value())

        Text(self.options[self.choice].name, Point(self.selectedposition.x+18, 8)).print_me(self.screen)

    def up(self):
        if not self.selected:
            self.soundManager.play_sound('menumove.wav')
            if self.choice-2 >= 0:
                self.choice -= 2

    def down(self):
        if not self.selected:
            self.soundManager.play_sound('menumove.wav')
            if self.choice+2 < len(self.options):
                self.choice += 2

    def right(self):
        if not self.selected:
            self.soundManager.play_sound('menumove.wav')
            self.choice += 1
            if self.choice >= len(self.options):
                self.choice = len(self.options)-1

    def left(self):
        if not self.selected:
            self.soundManager.play_sound('menumove.wav')
            self.choice -= 1
            if self.choice < 0:
                self.choice = 0

    def enter(self):
        self.soundManager.play_sound(str(self.options[self.choice].index)+'.wav')
        self.cursor = None
        self.selected = True

    def cancel(self):
        self.soundManager.play_sound('menucancel.wav')
        self.cursor = pygame.image.load(self.cursorpath).convert_alpha()
        self.selected = False

class CharSelector:
    def __init__(self, screen, screenManager, soundManager, cursor, background):
        self.p1 = CharMenu(screen, screenManager, soundManager, cursor, Point(40, 150), Point(22,22))
        self.p2 = CharMenu(screen, screenManager, soundManager, cursor, Point(216, 150), Point(202,22))
        self.screen = screen
        self.screenManager = screenManager
        self.soundManager = soundManager
        self.background = background

    def print_me(self):
        self.p1.print_me()
        self.p2.print_me()

    def mainloop(self):
        background = pygame.image.load('img/Background/' + self.background).convert()
        while True:
            if self.p1.selected and self.p2.selected:
                pygame.time.wait(2000)
                print('comecar luta')
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.soundManager.play_sound('menucancel.wav')
                        return 0
                    if event.key == K_UP:
                        self.p2.up()
                    if event.key == K_DOWN:
                        self.p2.down()
                    if event.key == K_RIGHT:
                        self.p2.right()
                    if event.key == K_LEFT:
                        self.p2.left()
                    if event.key == K_RETURN:
                        self.p2.enter()
                    if event.key == K_BACKSPACE:
                        self.p2.cancel()
                    if event.key == K_w:
                        self.p1.up()
                    if event.key == K_s:
                        self.p1.down()
                    if event.key == K_d:
                        self.p1.right()
                    if event.key == K_a:
                        self.p1.left()
                    if event.key == K_TAB:
                        self.p1.enter()
                    if event.key == K_q:
                        self.p1.cancel()

            self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            self.print_me()
            self.screenManager.display_update(self.screen)