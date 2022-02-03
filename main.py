# coding=utf-8
''' Author - Torkel Syversen '''
import pygame
import config
import game
import menu


class State:
    ''' Game state which renders and update other objects,
        depending on which state is set '''
    def __init__(self):
        self.state = None
        self.controls = ({})

    def render(self, surface, fps):
        ''' Renders state, with surface and fps given '''
        self.state.render(surface, fps)

    def update(self, delta):
        ''' Updates state with delta time given '''
        self.state.update(delta)

    def set_controls(self, player, id, key):
        ''' Set controls defined in the settings menu.
            This stores controls in a dictionary with the player number as key.
            If the player number is not defined, it creates a new dictionary.
         '''
        s = self.controls.get(player)
        if s is None:
            dict = ({player:({"thrust":0,"fire":0,"r_l":0,"r_r":0})})
            r = dict.get(player)
            for name, value in r.items():
                if name == id:
                    r[name] = key
            dict.update(r)
            self.controls.update(dict)
        else:
            r = self.controls.get(player)
            for name, value in r.items():
                if name == id:
                    r[name] = key
            self.controls.update(r)


    def check_state(self, main):
        ''' Check for any new state changes '''
        if self.state.done:
            if self.state.id == "game":
                self.set_state(menu.GameOver(self.state.players))

            elif self.state.id == "settings":
                self.set_state(menu.Settings())

            elif self.state.id == "next":
                self.set_state(menu.SettingsNext(self.controls))

            elif self.state.id == "quit":
                return True

            elif self.state.id == "continue":
                self.set_state(menu.Menu())

            elif self.state.id == "start":
                self.set_state(game.Mayhem(main.surface, self.controls))

    def set_state(self, state):
        ''' Set state to a given state '''
        self.state = state

    def get_state(self):
        ''' Returns current state '''
        return self.state

    def get_id(self):
        ''' Returns current id of the state '''
        return self.state.id



class Main:
    '''
        The game loop class.
        Game will automatically run once instanced.

    '''
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(config.screen_size)
        self.time = pygame.time.Clock()
        self.fps = config.fps
        self.running = False
        self.state = State()

        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_allowed(pygame.KEYUP)
        pygame.event.set_allowed(pygame.KEYDOWN)

        self.run()

    def run(self):
        ''' This function contains the game loop.
            The state set to run is the main menu.
         '''
        self.running = True
        #self.state.set_state(game.Mayhem(self.surface))
        self.state.set_state(menu.Menu())

        while self.running:
            self.surface.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(menu.Menu())
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.state.get_id() == "settings":
                        self.state.get_state().apply(self)

                    elif self.state.get_id() == "next":
                        self.state.get_state().apply(self)
                if event.type == pygame.KEYUP:
                    if self.state.get_id() == "next":
                        self.state.get_state().set_key(event.key, self.state)


            # Updates game with delta time give
            self.state.update(self.time.get_time()/1000)

            # Check for state updates
            if self.state.check_state(self):
                return self.quit()

            # Renders game with surface give
            self.state.render(self.surface, int(self.time.get_fps()))

            # Update time and display
            self.time.tick(self.fps)
            pygame.display.update()

    def quit(self):
        ''' Uninitializes pygame '''
        pygame.quit()


if __name__ == '__main__':
    print("Starting Mayhem")
    game = Main()
    print("Quitting")



















#s
