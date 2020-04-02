import pygame
import os


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def value(self):
        return (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __add__(self, other):
        if isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        else:
            return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Point(self.x - other[0], self.y - other[1])
        else:
            return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert (isinstance(other, int))
        return Point(self.x * other, self.y * other)

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        assert (isinstance(other, int))
        return Point(self.x // other, self.y // other)

    def __str__(self):
        return "Point({0}, {1})".format(self.x, self.y)


class SpriteSheetLoader:
    def __init__(self, file, sprite_width, sprite_height, fullsheet = False):
        self.sheet = pygame.image.load(os.path.join(file))
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprite_list = self.makeSpritelist()
        if not fullsheet:
            self.removeBlanks(file)

    def getSpriteList(self):
        return self.sprite_list

    def makeSprite(self,line=0,column=0):
        sprite = pygame.Surface((self.sprite_width, self.sprite_height)).convert_alpha()
        sprite.fill((0,0,0,0))
        sprite.blit(self.sheet, (-(column*self.sprite_width),-(line*self.sprite_height)))
        return sprite

    def makeSpritelist(self):
        size = self.sheet.get_size()
        sprite_list=[]
        for i in range(int(size[1]/self.sprite_height)):
            sprite_line=[]
            for j in range(int(size[0]/self.sprite_width)):
                sprite_line.append(self.makeSprite(i,j))
            sprite_list.append(sprite_line)
        return sprite_list

    def testBlankSprite(self, sprite):
        for i in range(self.sprite_width):
            for j in range(self.sprite_height):
                if sprite.get_at((i, j)) != (0, 0, 0, 0):
                    return False
        return True

    def removeBlanks(self, file):
        try:
            with open(file.replace('.png', '.txt'), encoding='utf-8') as txtfile:
                i=0
                for line in txtfile:
                    length = int(line)
                    while length < len(self.sprite_list[i]):
                        self.sprite_list[i].pop()
                    i+=1
        except:
            print('creating...')
            for sprite_line in self.sprite_list:
                j=0
                while j < len(sprite_line):
                    if self.testBlankSprite(sprite_line[j]):
                        sprite_line[j] = None
                    j+=1
            self.write(file)

    def write(self,file):
        txtfile = open(file.replace('.png', '.txt'), mode='w', encoding='utf-8')
        for sprite_line in self.sprite_list:
            i=0
            for sprite in sprite_line:
                if sprite == None:
                    break
                else: i+=1
            txtfile.write(str(i))
            txtfile.write('\n')