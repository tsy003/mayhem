A copy of the game Mayhem

How to launch:
The game runs from the main.py file.
In terminal type: 
	python3 main.py


General:
The config file includes different game variables which are editable for tweaking.
The most useful ones are already implemented in the game settings and can be set after starting the game.

Local multiplayer on same machine is set to a limit of 4 players in the settings menu.
However there is no actual limit to this, it can be changed to whatever in the config file.

Map layout:
The game map is created from the representation of the elements in the map_layout list.
Every element in the list represent 10% of the world width and height in their
x, y position.

Note:
Map layout needs a fuel pad for each player.
pygame.init() might take a while to load on windows






