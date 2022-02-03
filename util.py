# coding=utf-8
''' Author - Torkel Syversen, University of Tromsø '''

import pygame
import math
import random
import os




def load_file(string):
    ''' Load file from file name located in assets '''
    try:
        return pygame.image.load(os.path.join('assets', string))
    except:
        print("Error loading file")
        return None

# Sprites
player1 = load_file("player.png")
landing_pad = load_file("landing_pad.png")
object = load_file("rock.png")
rocky_island = load_file("rocky_island.png")
planet = load_file("bg_planet.png")
bullet = load_file("bullet.png")
bg_menu = load_file("cool.png")


def get_cos(v):
    return math.cos(v)

def mouse_over_button(mouse, obj):
    if mouse[0] >= obj.button.x and mouse[0] <= obj.button.x + obj.button.width and mouse[1] >= obj.button.y and mouse[1] <= obj.button.y + obj.button.height:
        return True, obj.id
    return False, None

def random_int(start, end):
    return random.randrange(start, end)

def distance(v1, v2):
    return ((v1.x-v2.x) * (v1.x-v2.x))+((v1.y-v2.y) * (v1.y-v2.y))

def lerp(a, b, c):
    '''Lerp a to b, based on percentage c (between 0, 1)'''
    return b*c + (1.0-c)*a


def get_angle(v2):
    ''' Get angle from a vector '''
    return math.degrees(math.atan2(-v2.x, -v2.y))

def set_vel(vel, angle):
    ''' Set vel direction from a given angle '''
    vel.x = -math.sin(math.radians(angle))
    vel.y = -math.cos(math.radians(angle))



# s
