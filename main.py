#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:
#
# Author:      crazzzypeter
#
# Created:     09.09.2021
# Copyright:   (c) crazzzypeter 2021
# Licence:     GNU GPL 3
#-------------------------------------------------------------------------------
import pygame
import colorsys

from pygame import gfxdraw
from pygame import draw_py
from dataclasses import dataclass


import random
import math

WIDTH=320*2
HEIGHT=240*2
FADEDISTANCE=100
POINTSCOUNT=50


class Point(pygame.math.Vector2):
    dx: float = 0.0
    dy: float = 0.0

def calc_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

points = []

def init():
    for _ in range(POINTSCOUNT):
        point = Point(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        angle = random.uniform(0, math.pi)
        point.dx = math.cos(angle) * 4
        point.dy = math.sin(angle) * 4
        points.append(point)

def update():
    for point in points:
        # перемещаем точку в соответсвии со скоростью
        point.x = point.x + point.dx;
        point.y = point.y + point.dy;

        # обрабатываем вылет за экран
        if point.x < 0:
            point.dx = abs(point.dx)
        if point.x > WIDTH:
            point.dx = -abs(point.dx)
        if point.y < 0:
            point.dy = abs(point.dy)
        if point.y > HEIGHT:
            point.dy = -abs(point.dy)


def draw(surface, alpha_surface, color):
    r,g,b = color
    alpha_surface.fill([0,0,0,0])
    for i in range(0, len(points)):
        for j in range(i + 1, len(points)):
            # вычисляем расстояние между линиями в -00 -> 0..1
            d = calc_distance(points[i], points[j])
            fade = -(calc_distance(points[i], points[j]) - FADEDISTANCE) / FADEDISTANCE

            # если фейд положителен рисуем
            if fade > 0 or d>10:
                for w in range( int(fade * 5+1) ) :

                    pygame.draw.aaline(
                        alpha_surface,
                        (r, g, b, int(fade * 255)),
                        pygame.Vector2(points[i].x+w, points[i].y-w),
                        pygame.Vector2(points[j].x+w, points[j].y-w)
                        #int(fade * 5 + 1)
                    )
        pygame.draw.circle(alpha_surface, (r, g, b, 0), (points[i].x, points[i].y), 5)
    surface.blit(alpha_surface, (0,0))

    #for point in points:
    #    pygame.draw.circle(surface, (0, 255, 100, 0), (point.x, point.y), 5)

def main():
    pygame.init()
    surface = pygame.display.set_mode(size=(WIDTH,HEIGHT), flags= \
        pygame.DOUBLEBUF | pygame.HWSURFACE
        )
    clock = pygame.time.Clock()

    is_running = True

    init()

    hue = 0.5
    alpha_surface = pygame.Surface(surface.get_size(), pygame.HWSURFACE )
    while is_running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        update()

        # draw
        surface.fill([0,0,0]) # white background
        hue +=0.005
        if(hue>=1):
            hue=0
        r,g,b = colorsys.hsv_to_rgb(hue,1,255)
        color = int(r),int(g),int(b)
        #color =(0,0,128)

        draw(surface, alpha_surface,color)

        clock.tick(60)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
