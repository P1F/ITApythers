import pygame
from pygame.locals import *
from char import Hitbox

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

pygame.init()
pygame.mixer.init()

screen = pygame.Surface((320, 240), 0, 32)

aux = pygame.display.set_mode((640, 480), 0, 32)

pos1 = Hitbox(30, 15, True)

pos2 = Hitbox(20, 10, False)

a = pygame.Surface((pos1.width, pos1.height), 0, 32)
a.fill((0, 100, 0))

b = pygame.Surface((pos2.width, pos2.height), 0, 32)
b.fill((0, 0, 100))

i = 0

while 1:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                pos2.y -= 1
            elif event.key == K_DOWN:
                pos2.y += 1
            elif event.key == K_RIGHT:
                pos2.x += 1
            elif event.key == K_LEFT:
                pos2.x -= 1
            elif event.key == K_w:
                pos1.y -= 1
            elif event.key == K_s:
                pos1.y += 1
            elif event.key == K_d:
                pos1.x += 1
            elif event.key == K_a:
                pos1.x -= 1
            if collide(pos1, pos2):
                print(str(i) + ' collide')
            else:
                print(str(i) + ' not collide')
            i += 1
        elif event.type == QUIT:
            exit()

    screen.fill((0, 0, 0))

    screen.blit(a, (pos1.x, pos1.y))
    screen.blit(b, (pos2.x, pos2.y))

    adjNewScreen = pygame.transform.scale2x(screen)
    aux.blit(adjNewScreen, (0, 0))
    pygame.display.update()