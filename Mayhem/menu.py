# coding=utf-8
''' Author - Torkel Syversen '''
import pygame
from pygame import Vector2
import text
import config
import util
import emitter
import random


class BaseButton:
    ''' Creates a rectangle, used for inheritance '''
    def __init__(self, x, y, w, h):
        self.button = pygame.Rect(int(x-w/2), int(y-h/2), w, h)
        self.button_color = (0, 0, 0)
        self.normal_color = (0, 0, 0)
        self.mouse_over_c = (0, 20, 20)


class Button(BaseButton):
    ''' Creates a clickable button, with label centered '''
    def __init__(self, id,  x, y, txt, size, w=150, h=50):
        super().__init__(x, y, w, h)
        self.id = id
        self.label = text.Label('Ariel', size)
        self.text = txt
        self.text_middle_x = self.button.centerx - self.label.get_size(txt)[0]/2
        self.text_middle_y = self.button.centery - self.label.get_size(txt)[1]/2
        self.is_clicked = False

    def set_text(self, txt):
        self.text = txt
        self.text_middle_x = self.button.centerx - self.label.get_size(txt)[0]/2
        self.text_middle_y = self.button.centery - self.label.get_size(txt)[1]/2

    def render(self, surface):
        pygame.draw.rect(surface, self.button_color, self.button)
        self.label.render(surface, self.text, self.text_middle_x, self.text_middle_y)

    def update(self, state):
        mouse = pygame.mouse

        check = util.mouse_over_button(mouse.get_pos(), self)
        if check[0]:
            self.button_color = self.mouse_over_c
        else: self.button_color = self.normal_color

        if not self.is_clicked:
            if mouse.get_pressed()[0] and check[1] == self.id:
                state.id = self.id
                state.done = True
                self.is_clicked = True

class ButtonAdded(Button):
    def __init__(self, x, y, txt, size, w=150, h=50):
        super().__init__("none", x, y, txt, size, w, h)

    def update(self, state):
        mouse = pygame.mouse

        check = util.mouse_over_button(mouse.get_pos(), self)
        if check[0]:
            self.button_color = self.mouse_over_c
        else: self.button_color = self.normal_color


class SettingButton:
    def __init__(self, id, list, h_txt, x, y, size, i=0):
        self.id = id
        self.done = False

        self.iter = i
        self.list = list
        self.x = x
        self.y = y
        self.header_text = h_txt
        self.header = text.Label('Ariel', 30)
        self.header.set_color((30, 200, 0))

        self.main = ButtonAdded(x, y, "txt", 30)
        w = self.get_config(self.id)
        self.main.set_text(w)

        # Get iter on correct position
        p = 0
        for i in self.list:
            if i == w:
                self.iter = p
                break
            else: p += 1

        self.l = ButtonAdded(x-100, y, "<-", 20, w=50)
        self.r = ButtonAdded(x+100, y, "->", 20, w=50)

    def get_config(self, id):
        d = ({"fps":config.fps,
         "players":config.players,
         "gravity":config.gravity,
         "play_time":config.play_time,
         "thrust_power":config.thrust_power,
         "fuel_consume":config.fuel_consume,
         "rotate_speed":config.rotate_speed
         })
        for key, item in d.items():
            if key == id:
                return str(item)
        return "glitch"

    def set_config(self, main):
        if self.id == "fps":
            config.fps = int(self.main.text)
            main.fps = config.fps
        elif self.id == "players":
            config.players = int(self.main.text)
        elif self.id == "gravity":
            config.gravity = int(self.main.text)
        elif self.id == "play_time":
            config.play_time = int(self.main.text)
        elif self.id == "thrust_power":
            config.thrust_power = int(self.main.text)
        elif self.id == "fuel_consume":
            config.fuel_consume = int(self.main.text)
        elif self.id == "rotate_speed":
            config.rotate_speed = int(self.main.text)



    def render(self, surface):
        self.header.render(surface, self.header_text, self.x-int(self.header.get_size(self.header_text)[0]/2), self.y-50)
        self.main.render(surface)
        self.l.render(surface)
        self.r.render(surface)

    def update(self):
        self.main.update(self)
        self.l.update(self)
        self.r.update(self)
    def add(self, x, main):
        self.iter += x
        if self.iter < 0:
            self.iter = 0
        elif self.iter > len(self.list)-1:
            self.iter = len(self.list)-1
        self.main.set_text(self.list[self.iter])
        self.set_config(main)

class Settings:
    def __init__(self):
        self.id = "settings"
        self.done = False
        self.mx = config.screen_size[0]/2
        self.my = config.screen_size[1]
        self.general_header = text.Label('Ariel', 50)
        self.general_header.set_color((20, 20, 0))
        self.player_header = text.Label('Ariel', 50)
        self.player_header.set_color((20, 20, 0))
        self.header = text.Label('Ariel', 80)
        self.header.set_color((255, 255, 0))
        self.back_button = Button("continue", self.mx, self.my-100, "Back", 30)
        self.next_button = Button("next", self.mx+self.mx/2, self.my-100, "Player Controls", 30, w=200)

        # Buttons
        fps_list = ["120", "150", "180", "210", "300", "500"]
        players_list = ["1", "2", "3", "4"]
        play_time_list = ["60", "120", "150", "180", "210", "300", "500", "1000"]
        gravity_list = ["0", "20", "40", "60", "80", "100", "150"]
        speed_list = ["200", "250", "300", "400", "500"]
        fuel_c_list = ["1", "2", "4", "6", "8", "10", "14", "18", "25"]
        rotate_list = ["50", "80", "120", "180", "200", "250", "300"]

        posx = int(self.mx/2)
        posy = 200+40
        #pos1 = int(config.screen_size[0]/3)

        # General
        self.fps_button = SettingButton("fps", fps_list, "FPS", posx, posy, "s", 30)
        self.players_button = SettingButton("players", players_list, "Multiplayer", posx*2, posy, "s", 30)
        self.play_time_button = SettingButton("play_time", play_time_list, "Match time (seconds)", posx*3, posy, "s", 30)
        # player
        self.gravity_button = SettingButton("gravity", gravity_list, "Gravity", posx-180, posy+posy, "s", 30)
        self.speed_button = SettingButton("thrust_power", speed_list, "Speed", posx*2-180, posy+posy, "s", 30)
        self.fuel_c_button = SettingButton("fuel_consume", fuel_c_list, "Fuel consume", posx*3-180, posy+posy, "s", 30)
        self.rotate_button = SettingButton("rotate_speed", rotate_list, "Rotate speed", posx*4-180, posy+posy, "s", 30)

        self.b_list = [self.fps_button, self.players_button, self.play_time_button, self.gravity_button, self.speed_button, self.fuel_c_button, self.rotate_button]

    def apply(self, main):
        m = pygame.mouse
        for i in self.b_list:
            is_over_l = util.mouse_over_button(m.get_pos(), i.l)
            is_over_r = util.mouse_over_button(m.get_pos(), i.r)
            if is_over_l[0]:
                i.add(-1, main)
                return
            elif is_over_r[0]:
                i.add(1, main)
                return

    def render(self, surface, _):
        self.header.render(surface, "Settings", self.mx-self.header.get_size("Settings")[0]/2, 40)
        self.general_header.render(surface, "General config", self.mx-self.general_header.get_size("General config")[0]/2, 120)
        pygame.draw.line(surface, (20, 20, 0), (0, 160), (config.screen_size[0], 160), 3)
        self.player_header.render(surface, "Player config", self.mx-self.player_header.get_size("Player config")[0]/2, 350)
        pygame.draw.line(surface, (20, 20, 0), (0, 390), (config.screen_size[0], 390), 3)
        self.back_button.render(surface)
        self.next_button.render(surface)

        for i in self.b_list:
            i.render(surface)


    def update(self, delta):

        self.id = "settings"
        self.back_button.update(self)
        self.next_button.update(self)
        for i in self.b_list:
            i.update()

class InputButton(Button):
    #id,  x, y, txt, size, w=150, h=50
    def __init__(self, player, id, x, y, txt, h_txt, size, w=150, h=50):
        super().__init__(id, x, y, txt, size, w, h)
        self.player = player
        self.clicked_color = (0, 150, 0)
        self.mx = x
        self.my = y
        self.header = text.Label('Ariel', 20)
        self.header.set_color((30, 90, 120))
        self.t = h_txt
        self.t_w = int(self.header.get_size(h_txt)[0]/2)

    def render(self, surface):
        super().render(surface)
        self.header.render(surface, self.t, self.mx-self.t_w, self.my-40)

    def update(self):
        mouse = pygame.mouse

        check = util.mouse_over_button(mouse.get_pos(), self)
        if check[0] and not self.is_clicked:
            self.button_color = self.mouse_over_c
        elif not self.is_clicked:
            self.button_color = self.normal_color


    def apply(self, b_list, current):
        mouse = pygame.mouse
        check = util.mouse_over_button(mouse.get_pos(), self)

        if not self.is_clicked:
            if check[0] and check[1] == self.id:
                for i in b_list:
                    for s in i:
                        s.is_clicked = False
                self.button_color = self.clicked_color
                self.is_clicked = True
                return self
        return current



class SettingsNext:
    #self, id,  x, y, txt, size, w=150, h=50
    def __init__(self, controls):
        self.done = False
        self.id = "next"
        self.mx = int(config.screen_size[0]/2)
        self.my = int(config.screen_size[1]/2)
        self.current = None
        self.back = Button("settings", self.mx-200, config.screen_size[1]-100, "Back", 30)


        self.header_list = []
        self.list = []
        x = -200
        y = -100
        for i in range(0, config.players):
            header = text.Label('Ariel', 40)
            header.set_color((0, 150, 0))
            header.text = "Player "+str(i+1)
            header.posx = self.mx-100+x-header.get_size(header.text)[0]/2
            header.posy = self.my-200+y
            self.header_list.append(header)

            current_controls = []
            c = controls.get(i+1)
            if c is not None:
                current_controls.append(pygame.key.name(c.get("thrust")))
                current_controls.append(pygame.key.name(c.get("fire")))
                current_controls.append(pygame.key.name(c.get("r_l")))
                current_controls.append(pygame.key.name(c.get("r_r")))
            else:
                current_controls.append("empty")
                current_controls.append("empty")
                current_controls.append("empty")
                current_controls.append("empty")

            thrust = InputButton(i, "thrust", self.mx-200+x, self.my-100+y,current_controls[0], "Thrust", 30)
            fire = InputButton(i, "fire", self.mx+x, self.my-100+y,current_controls[1], "Fire", 30)
            r_l = InputButton(i, "r_l", self.mx-200+x, self.my+y,current_controls[2], "Rotate left", 30)
            r_r = InputButton(i, "r_r", self.mx+x, self.my+y,current_controls[3], "Rotate right", 30)
            self.list.append([thrust, fire, r_l, r_r])
            if x > -200:
                y += 300
                x = -200-400
            x += 400

    def apply(self, state):
        for i in self.list:
            for s in i:
                self.current = s.apply(self.list, self.current)

    def set_key(self, key, state):
        if self.current is not None:
            s = pygame.key.name(key)
            self.current.set_text(s)
            state.set_controls(self.current.player+1, self.current.id, key)

    def render(self, surface, _):
        for i in self.list:
            for s in i:
                s.render(surface)

        for x in self.header_list:
            x.render(surface, x.text, x.posx, x.posy)
        self.back.render(surface)

    def update(self, delta):
        self.id = "next"
        for i in self.list:
            for s in i:
                s.update()
        self.back.update(self)

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.id = "menu"
        self.done = False
        self.mx = config.screen_size[0]/2
        self.my = config.screen_size[1]/2
        self.header = text.Label('Ariel', 80)
        self.header.set_color((255, 255, 0))
        self.start_button = Button("start", self.mx, self.my-100, "Start Game", 30)
        self.settings_button = Button("settings", self.mx, self.my, "Settings", 30)
        self.quit_button = Button("quit", self.mx, self.my+100, "Quit", 30)

        self.emitter = emitter.Emitter()
        self.emitter.add_rect(500, 0, 0, config.screen_size[0],config.screen_size[1])
        self.emitter.color = (120, 120, 0)

        self.group = pygame.sprite.Group()
        self.size = (500, 500)
        self.sprite = pygame.sprite.Sprite()
        self.original = pygame.transform.scale(util.bg_menu, self.size)
        self.sprite.image = pygame.transform.scale(self.original, self.size)
        self.sprite.rect = self.sprite.image.get_rect()
        self.group.add(self.sprite)

        self.bg_pos = Vector2(0, 0)
        self.end_pos = Vector2(config.screen_size[0]/2-250,900)
        self.time = 0
        self.angle = 0


    def render(self, surface, _):
        size = self.header.get_size("Mayhem")
        self.header.render(surface, "Mayhem", self.mx-size[0]/2, 40)
        self.start_button.render(surface)
        self.settings_button.render(surface)
        self.quit_button.render(surface)
        self.emitter.render(surface, Vector2(0, 0))

        self.group.draw(surface)


    def update(self, delta):
        self.id = "menu"
        self.start_button.update(self)
        self.settings_button.update(self)
        self.quit_button.update(self)

        self.emitter.add_rect(1, 0, 0, config.screen_size[0],config.screen_size[1])
        self.emitter.update(delta)
        self.bg_pos = self.bg_pos.lerp(self.end_pos, delta)
        self.time += delta
        self.end_pos.x += util.get_cos(self.time)*5
        self.end_pos.y = util.get_cos(self.time)*20
        self.angle += 30*delta
        self.angle = self.angle % 360
        self.sprite.image = pygame.transform.rotate(self.original, self.angle)
        self.sprite.rect.x = self.bg_pos.x
        self.sprite.rect.y = self.bg_pos.y




class GameOver:
    def __init__(self, players):
        self.id = "gameover"
        self.done = False

        self.continue_button = Button("continue", config.screen_size[0]/2, config.screen_size[1]-100, "Continue", 30)

        self.players = []
        self.highest_score = -2000
        self.winner = []
        for player in players:
            if player.score > self.highest_score:
                self.highest_score = player.score
                self.winner = [player]
            elif player.score == self.highest_score:
                self.winner.append(player)

            self.players.append(player)

        # Top label
        self.header_top = text.Label('Ariel', 80)
        self.header_top.set_color((255, 255, 0))

        self.top_player_label = []

        s = text.Label('Ariel', 40)
        s.set_color((0, 255, 255))
        x = text.Label('Ariel', 40)
        x.set_color((255, 255, 0))
        y = text.Label('Ariel', 40)
        y.set_color((255, 255, 0))
        z = text.Label('Ariel', 40)
        z.set_color((255, 255, 0))
        self.top_player_label.append(s)
        self.top_player_label.append(x)
        self.top_player_label.append(y)
        self.top_player_label.append(z)



    def render(self, surface, fps):
        if len(self.winner) > 1:
            txt = "Top players"
            self.header_top.render(surface, txt, config.screen_size[0]/2-self.header_top.get_size(txt)[0]/2, 50)
        else:
            txt = "Top player"
            self.header_top.render(surface, txt, config.screen_size[0]/2-self.header_top.get_size(txt)[0]/2, 50)

        y = 0
        for s in self.winner:
            player = ("Player ", s.player)
            bullets_fired = ("Bullets fired: ", s.bullets_fired)
            distance_traveled = ("Distance traveled: ", int(s.distance_traveled))
            score = ("Score: ", s.score)
            list = [player, bullets_fired, distance_traveled, score]
            for i in self.top_player_label:
                text = list[0][0]+str(list[0][1])
                i.render(surface, text, int(config.screen_size[0]/2-i.get_size(text)[0]/2), 150+y)
                if len(list)>1:
                    del list[0]
                y += 40
            y += 40

        self.continue_button.render(surface)


    def update(self, delta):
        self.id = "gameover"
        self.continue_button.update(self)











#
