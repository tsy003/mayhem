# coding=utf-8
''' Author - Torkel Syversen '''

# ~~~~~ General ~~~~~ #
# X should be twice as big as Y value
# for 2 players, (three times for 3 player, etc..)
screen_size = (1800, 700)
play_time = 120 # seconds
fps = 180

# ~~~~~ Screen divide properties ~~~~~ #
divide_color = (255, 250, 0)
divide_width = 5


# ~~~~~ Debug ~~~~~ #
debug = False

# ~~~~~ Multiplayer ~~~~~ #
# Can be unlimited players,
# but the spawning system is a bit glitchy
players = 1

# ~~~~~ Player configs ~~~~~ #
bullet_speed = 500
thrust_power = 200
rotate_speed = 180
fuel_consume = 1
max_fuel = 100
start_fuel = 50
gravity = 50


# ~~~~~ Map ~~~~~ #
# Map size from origin (0, 0)
map_size = (2500, 2500)
map_bound_color = (0, 255, 100)
map_bound_width = 5
# Boolean to use map_layout below
use_layout = False
map_layout = [
# Layout of map
# t = top wall
# b = bot wall
# r = rocky island
# p = landing pad/fuel pad
# y = huge planet
# Everything else is free space(10% of map size)
# ONLY REQUIREMENT:
# There needs to be enough landing pads for each player
"t","0","0","0","0","0","0","0","0","t",
"0","p"," ","p","0","0","0","0","0","0",
"0","0","0","0","0","0","0","0","0","0",
"0","0","0","0","0","0","0","0","0","0",
"0","0","0","p","0","0","0","0","0","0",
"0","0","0","0","0","p","0","0","0","0",
"0","0","0","0","0","0","0","0","0","0",
"0","0","0","0","0","0","0","0","0","0",
"0","0","0","0","0","0","0","0","0","0",
"t","0","0","0","0","0","0","0","0","t",
]













# s
