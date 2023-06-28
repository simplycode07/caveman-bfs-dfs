import pygame
import os
import csv

pygame.init()
display_size = (640,640)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption("Cave-Man OONGA BOONGA")

clock = pygame.time.Clock()

def check_collision(tilemap, offset_x, offset_y, sprite_x, sprite_y):
    restrict_move = []
    if tilemap[offset_y+sprite_y-1][offset_x+sprite_x] == '1':
        restrict_move.append("w")
    if tilemap[offset_y+sprite_y+1][offset_x+sprite_x] == '1':
        restrict_move.append("s")
    if tilemap[offset_y+sprite_y][offset_x+sprite_x+1] == '1':
        restrict_move.append("d")
    if tilemap[offset_y+sprite_y][offset_x+sprite_x-1] == '1':
        restrict_move.append("a")

    return restrict_move

def read_map(filename):
    tilemap = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=",")
        for row in data:
            tilemap.append(list(row))
        return tilemap

walls_rect = []

def draw_rect(map, ground, stone, offset_x, offset_y):
    for x in range(20):
        for y in range(20):
            square_rect = pygame.Rect(32*(x), 32*(y), 32, 32)
            if  map[y+offset_y][x+offset_x] == '1':
                display.blit(stone, square_rect)
            else:
                display.blit(ground, square_rect)

def main():
    angle = 0
    change_angle = 0
    map = read_map("tilemap.csv")
    ground = pygame.image.load("ground.png").convert()
    walls = pygame.image.load("walls.png").convert()
    sprite_original = pygame.image.load("sprite.png").convert()
    sprite_rotated = pygame.image.load("sprite.png").convert()
    sprite_x = 10
    sprite_y = 10
    offset_x_max = len(map[0])-20
    offset_y_max = len(map)-20
    offset_x = offset_x_max//2
    offset_y = offset_y_max//2
    while 1:
        for event in pygame.event.get():
            restrict_move = check_collision(map,offset_x, offset_y,sprite_x, sprite_y)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.unicode == 'w':
                    change_angle = 90
                    if not ("w" in restrict_move):
                        if (offset_y == 0 and sprite_y > 0) or (offset_y == offset_y_max and sprite_y > 10):
                            sprite_y -= 1
                        elif offset_y > 0:
                            offset_y -= 1
                elif event.unicode == 's':
                    change_angle = -90
                    if not ("s" in restrict_move):
                        if (offset_y == 0 and sprite_y < 10) or (offset_y == offset_y_max and sprite_y < 20):
                            sprite_y += 1
                        elif offset_y < 4:
                            offset_y += 1
                elif event.unicode == 'a':
                    change_angle = 180
                    if not ("a" in restrict_move):
                        if (offset_x == 0 and sprite_x > 0) or (offset_x == offset_x_max and sprite_x > 10) :
                            sprite_x -= 1
                        elif offset_x > 0:
                            offset_x -= 1
                elif event.unicode == 'd':
                    change_angle = 0
                    if not ("d" in restrict_move):
                        if (offset_x == 0 and sprite_x < 10) or (offset_x == offset_x_max and sprite_x < 20):
                            sprite_x += 1
                        elif offset_x < 10:
                            offset_x += 1

                sprite_rotated = pygame.transform.rotate(sprite_original, change_angle-angle)
                print(f"offset = ({offset_x}, {offset_y}), sprite = ({sprite_x}, {sprite_y})")

            draw_rect(map, ground, walls, offset_x, offset_y)
            sprite_rect = pygame.Rect(sprite_x*32,sprite_y*32,32,32)
            display.blit(sprite_rotated, sprite_rect)
            clock.tick(120)
            pygame.display.update()
            

main()