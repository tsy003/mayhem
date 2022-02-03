# coding=utf-8
''' Author - Torkel Syversen '''
import pygame
from pygame import Vector2
import config
import util
import emitter
import text



class Entity(pygame.sprite.Sprite):
    ''' Base class for all moving objects,
        Inherits from pygame.sprite.Sprite, which holds sprite objects
        and renders them
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.id = "entity"
        self.pos = Vector2(0, 0)
        self.center_pos = Vector2(0, 0)
        self.radius = 10
        self.remove = False
        self.angle = 100

    def rotate(self):
        ''' Rotate image, based on angle, does not resize image rect '''
        self.sprite.image = pygame.transform.rotate(self.original_img, self.angle)

    def rotate_fix(self):
        ''' Rotate image, based on angle, resizes image rect '''
        self.sprite.image = pygame.transform.rotate(self.original_img, self.angle)
        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.rect.center)

    def set_sprite(self, sprite, size):
        '''
            Set the sprite for the sprite class with size given.
            Saves the original image, scaled down to the size given
            and adds the sprite to group
        '''
        self.group = pygame.sprite.Group()
        self.original_img = sprite
        self.size = size
        self.original_img = pygame.transform.scale(self.original_img, self.size)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.transform.scale(self.original_img, self.size)
        self.sprite.rect = self.sprite.image.get_rect()
        self.group.add(self.sprite)

    def update(self, delta, x):
        ''' Set the sprite image to the current position '''
        self.sprite.rect.x = self.pos.x
        self.sprite.rect.y = self.pos.y

    def render(self, surface, cam):
        ''' Calls the group.draw function '''
        self.group.draw(surface)

    def apply_cam(self, cam):
        ''' Applies camera given to the image position '''
        self.sprite.rect.x += cam.x
        self.sprite.rect.y += cam.y

    def check_collision(self, obj):
        '''
            Return true if object given collides
            also applies score if the object hits a player
            Return false otherwise
        '''
        distance = util.distance(self.pos, obj.pos)
        if distance <= self.radius*self.radius:
            self.remove = True
            obj.remove = True
            if self.id == "bullet" and obj.id == "bullet":
                return True
            if self.id == "bullet":
                #obj.score -= 1
                self.player.score += 1
            elif obj.id == "bullet":
                #self.score -= 1
                obj.player.score += 1

            return True
        return False

    def debug_collision(self, surface, cam):
        '''
            Draws collision line.
            Note: the collision circle of moving objects
            is calculated as rects with applied radius
        '''
        pygame.draw.circle(surface, (0, 255, 0), (int(self.sprite.rect.centerx+cam.x), int(self.sprite.rect.centery+cam.y)), self.radius, 1)


class Object(Entity):
    ''' Base class for all NON moving objects.
        Inherits from Entity.
    '''
    def __init__(self):
        super().__init__()

    # def render(self, surface):
    #     self.group.draw(surface)


    def generate_collision_rects(self, pos, amount=20, dy=20):
        '''
            Generate collision lines, by looping through self.sprite.image.
            Creates a list of rects named collision_rects.
            pos = position of image as vector2.
            amount = max amount of lines to create.
            dy = height between each line.
        '''
        self.collision_rects = []
        img_width = self.sprite.image.get_width()
        img_height = self.sprite.image.get_height()
        img = self.sprite.image

        a = 0 # Amount of rects created

        for y in range(0, img_height, dy):
            if a >= amount:
                return

            for x in range(0, img_width):
                if a >= amount:
                    return

                c = img.get_at((x, y))
                if c[0] > 0 or c[1] > 0 or c[2] > 0 or c[3] > 50:

                    for w in range(img_width-1, x, -1):
                        p = img.get_at((w, y))
                        if p[0] > 0 or p[1] > 0 or p[2] > 0 or p[3] > 50:
                            self.collision_rects.append(pygame.Rect((pos.x+x, pos.y+y), (pos.x+w, pos.y+y)))
                            a += 1
                            break
                    break


    def check_collision(self, obj):
        ''' Check if obj given collide with any of the collision_rects '''
        for i in self.collision_rects:
            if obj.pos.x+obj.radius >= i.x and obj.pos.x-obj.radius <= i.width and obj.pos.y+obj.radius >= i.y and obj.pos.y-obj.radius <= i.height:
                obj.remove = True
                return

    def debug_collision(self, surface, cam):
        ''' Draw collision lines '''
        for i in self.collision_rects:
            pygame.draw.line(surface, (255, 255, 255), (i.x+cam.x, i.y+cam.y), (i.width+cam.x, i.y+cam.y))

class LandingPad(Object):
    '''
        Landing pad object, inherits from Object class.
        Generates collision rects when instanced.
    '''
    def __init__(self, sprite, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y
        self.size = (256, 128)
        self.radius = 130
        self.set_sprite(sprite, self.size)


        self.land_rect = [pygame.Rect((x, y), (x+self.sprite.rect.width, y+10))]
        self.generate_collision_rects(self.pos, amount=20, dy=15)
        #print(len(self.collision_rects))

    def check_collision(self, obj):
        ''' Redefines the check_collision function inherited,
            to be able to check if the player is fueling.
         '''
        for i in self.land_rect:
            if obj.pos.x+obj.radius >= i.x and obj.pos.x-obj.radius <= i.width and obj.pos.y+obj.radius >= i.y and obj.pos.y-obj.radius <= i.height:
                if obj.vel.y < 0:
                    #print(obj.angle)
                    if obj.angle <= 15 or obj.angle >= 345:
                        obj.on_pad = True
                        #print("on pad")
                        return

                obj.remove = True
                return
        super().check_collision(obj)


    def debug_collision(self, surface, cam):
        for i in self.land_rect:
            pygame.draw.line(surface, (0, 255, 0), (i.x+cam.x, i.y+cam.y), (i.width+cam.x, i.y+cam.y))
            pygame.draw.line(surface, (0, 255, 0), (i.width+cam.x, i.y+cam.y), (i.width+cam.x, i.height+cam.y))
            pygame.draw.line(surface, (0, 255, 0), (i.x+cam.x, i.height+cam.y), (i.x+cam.x, i.y+cam.y))

        super().debug_collision(surface, cam)

class Planet(Object):
    ''' Inherits from Object '''
    def __init__(self, sprite, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y
        #self.radius = 100
        #self.size = (int(config.map_size[0] * 0.1)+20, 100)
        self.size = (600, 600)
        self.set_sprite(sprite, self.size)
        self.generate_collision_rects(self.pos, amount=300, dy=40)
        #print(len(self.collision_rects))

class RockyIsland(Object):
    ''' Inherits from Object '''
    def __init__(self, sprite, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y
        #self.radius = 100
        #self.size = (int(config.map_size[0] * 0.1)+20, 100)
        self.size = (200, 300)
        self.set_sprite(sprite, self.size)
        self.generate_collision_rects(self.pos, amount=20, dy=15)
        #print(len(self.collision_rects))


class WallTop(Object):
    ''' Inherits from Object '''
    def __init__(self, sprite, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y
        self.radius = 100
        self.size = (int(config.map_size[0] * 0.1)+20, 100)
        self.set_sprite(sprite, self.size)
        self.generate_collision_rects(self.pos, amount=10, dy=10)
        #print(len(self.collision_rects))


class WallBot(Object):
    ''' Inherits from Object '''
    def __init__(self, sprite, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y
        self.radius = 100
        self.size = (int(config.map_size[0] * 0.1)+20, 100)
        self.set_sprite(sprite, self.size)
        self.angle = 180
        self.rotate()
        self.generate_collision_rects(self.pos, amount=10, dy=10)
        #print(len(self.collision_rects))


class Map:
    '''
        Creates the game map with map size from config file.
        The map layout represents the world, where each element
        has a width and height of 10% of the map size width and height.
    '''
    def __init__(self, sprite_group, collision, entity_list):
        # Map size from origin (0, 0)
        self.map_size = config.map_size
        self.map_objects = []
        self.landing_pads = []
        self.map_layout = [
        "t","t","0","r","0","0","0","0","0","b",
        "t","b","0","0","r","0","0","0","t","0",
        "0","t","t","0","0","0","r","0","0","t",
        "p","0","0","0","0","0","0","p","0","0",
        "b","b","b","0","0","0","t","0","0","0",
        "0","0","0","0","y","0","0","0","r","0",
        "0","0","0","t","0","0","0","0","0","0",
        "0","0","0","b","0","0","0","r","0","b",
        "0","p","0","0","t","0","p","0","0","0",
        "0","0","0","p","0","0","0","0","r","p",
        ]
        self.set_objects(sprite_group, collision, entity_list)

    def set_objects(self, sprite_group, collision, entity_list):
        '''Instanciate objects based on map layout,
            And stores them in sprite group, collision list, and entity list.
         '''
        if config.use_layout:
            self.map_layout = config.map_layout

        self.width = self.map_size[0] * 0.1 # 10% of map size
        self.height = self.map_size[1] * 0.1 # 10% of map size

        x = 0
        y = 0
        for i in self.map_layout:
            if x >= self.map_size[0]:
                y += self.height
                x = 0

            # Spawn object
            if i == "t":
                t = WallTop(util.object, x, y)
                sprite_group.add(t)
                collision.add_static(t)
                entity_list.append(t)

            elif i == "b":
                t = WallBot(util.object, x, y)
                sprite_group.add(t)
                collision.add_static(t)
                entity_list.append(t)

            # Spawn landing pad
            elif i == "p":
                t = LandingPad(util.landing_pad, x, y)
                sprite_group.add(t)
                collision.add_static(t)
                self.landing_pads.append(t)
                entity_list.append(t)

            # Spawn rocky island
            elif i == "r":
                t = RockyIsland(util.rocky_island, x, y)
                sprite_group.add(t)
                collision.add_static(t)
                entity_list.append(t)

            # Spawn planet
            elif i == "y":
                t = Planet(util.planet, x, y)
                sprite_group.add(t)
                collision.add_static(t)
                entity_list.append(t)


            x += self.width


    def render(self, surface, cam):
        '''
            Renders the map bounds.
        '''

        # Map bounds
        pygame.draw.line(surface, config.map_bound_color, (0+cam.x, 0+cam.y), (self.map_size[0]+cam.x, 0+cam.y), config.map_bound_width)
        pygame.draw.line(surface, config.map_bound_color, (self.map_size[0]+cam.x, 0+cam.y), (self.map_size[0]+cam.x, self.map_size[1]+cam.y), config.map_bound_width)
        pygame.draw.line(surface, config.map_bound_color, (self.map_size[0]+cam.x, self.map_size[1]+cam.y), (0+cam.x, self.map_size[1]+cam.y), config.map_bound_width)
        pygame.draw.line(surface, config.map_bound_color, (0+cam.x, self.map_size[1]+cam.y), (0+cam.x, 0+cam.y), config.map_bound_width)




class Collision:
    '''
        Class to handle collision.
        Dynamic objects = moving objects
        Static objects = non moving objects
    '''
    def __init__(self):
        self.dynamic_objs = []
        self.static_objs = []

    # Debug render
    def debug(self, surface, cam):
        for i in self.dynamic_objs:
            i.debug_collision(surface, cam)

        for i in self.static_objs:
            i.debug_collision(surface, cam)

    def update(self):
        '''
            Checks if dynamic objects collide with other dynamic objects
            and static objects.
            Static objects are not able to collide with themselves
            and are therefor not checked.
        '''
        for this in self.dynamic_objs:
            if this.remove and this.id == "bullet":
                self.remove(this)
                continue

            # Check bounds
            if this.pos.x-this.radius <= 0 or this.pos.x+this.radius >= config.map_size[0] or this.pos.y-this.radius <= 0 or this.pos.y+this.radius >= config.map_size[1]:
                this.remove = True
                continue

            next = False
            # Dynamic objects collision detection
            for obj in self.dynamic_objs:
                if obj is this:
                    continue


                # Check collision
                if obj.check_collision(this):
                    next = True
                    break


            if next:
                continue
            # Kinematic objects collision detection
            for obj in self.static_objs:
                obj.check_collision(this)



    def remove(self, obj):
        ''' Removes a dynamic object '''
        self.dynamic_objs.remove(obj)

    def add_static(self, obj):
        self.static_objs.append(obj)
    def add_dynamic(self, obj):
        self.dynamic_objs.append(obj)




class Bullet(Entity):
    ''' Bullet class, inherits from Entity '''
    def __init__(self, player, sprite):
        super().__init__()
        self.id = "bullet"
        self.size = (5, 5)
        self.set_sprite(sprite, self.size)

        self.player = player
        self.pos = Vector2(player.pos.x+player.vel.x*player.size[0]/2, player.pos.y+player.vel.y*player.size[1]/2)
        self.vel = Vector2(player.vel.x, player.vel.y)
        self.speed = config.bullet_speed
        self.radius = 4
        self.color = (255, 255, 255)
        self.life = 2.0

    def render(self, surface, cam):
        ''' Renders itself with applied camera position '''
        self.apply_cam(cam)
        self.group.draw(surface)
        self.apply_cam(-cam)

    def update(self, delta):
        if self.life <= 0.0:
            self.remove = True
        self.pos += self.speed*self.vel*delta
        self.life -= delta

        self.sprite.rect.x = self.pos.x
        self.sprite.rect.y = self.pos.y



class Player(Entity):
    ''' Player class inherits from Entity
        Upon instance, it create labels to show stats,
        and also sets the controls given in the settings.
        If no controls are given, defaults will be used.
     '''
    def __init__(self, sprite, player, screen_size, controls):
        super().__init__()

        # Collision radius
        # will be rect collision detection
        # with applied radius from center
        self.radius = 30
        self.on_pad = False
        self.score = 0
        self.bullets_fired = 0
        self.distance_traveled = 0

        # Font
        self.pos_label = text.Label('Ariel', 20)
        self.fps_label = text.Label('Ariel', 20)
        self.fuel_label = text.Label('Ariel', 30)
        self.fuel_label.set_color((0, 255, 0))
        self.score_label = text.Label('Ariel', 30)
        self.score_label.set_color((255, 255, 0))

        # Player type
        # Player1, player2, player3 etc
        self.player = player
        self.get_controls(controls)

        # self.original_img = sprite
        self.size = (64, 64)
        self.set_sprite(sprite, self.size)

        self.angle = 0
        self.cam = Vector2(0, 0)
        self.pos = Vector2(screen_size.x/2, screen_size.y/2)
        self.vel = Vector2(0, 0)
        self.screen_size = screen_size

        self.thrust = 0
        self.gravity = config.gravity
        self.fuel = config.start_fuel
        self.max_fuel = config.max_fuel
        self.fuel_pos = (20, config.screen_size[1]-30)
        self.fuel_length = self.fuel
        self.fuel_multiplier = (config.screen_size[0]/config.players)*0.005


        self.emitter = emitter.Emitter()
        # Timer to add particles
        self.p_add_time = 0.1
        self._p_timer = self.p_add_time

        # Bullet properties
        self.bullets = []
        self.bullet_cooldown = 0.2 # seconds
        self._timer = 0

    def reset_pos(self):
        ''' Reset pos and cam pos, and spawns particles '''
        self.emitter.add_rect(30, self.sprite.rect.x, self.sprite.rect.y, self.size[0], self.size[1])

        self.angle = 0
        self.cam.x = 0
        self.cam.y = 0
        self.fuel = config.start_fuel

        self.pos.x = self.screen_size.x/2
        self.pos.y = self.screen_size.y/2
        random = util.random_int(0, len(self.landing_pads))
        pad = self.landing_pads[random]
        posx = pad.pos.x-(pad.sprite.rect.width*3)/config.players+self.size[0]*config.players
        s = Vector2(posx, pad.pos.y-pad.sprite.rect.height*3)
        self.translate(s)


    def set_pos(self, pads):
        ''' Set pos to a random fuel pad, with fuel pad list given, also spawns particles '''

        self.angle = 0
        self.cam.x = 0
        self.cam.y = 0
        self.fuel = config.start_fuel

        self.pos.x = self.screen_size.x/2
        self.pos.y = self.screen_size.y/2
        random = util.random_int(0, len(pads))
        pad = pads[random]
        posx = pad.pos.x-(pad.sprite.rect.width*3)/config.players+self.size[0]*config.players
        s = Vector2(posx, pad.pos.y-pad.sprite.rect.height*3)
        self.translate(s)

        self.emitter.add_rect(100, self.pos.x-self.size[0]/2, self.pos.y-self.size[1]/2, self.size[0], self.size[1])
        return pad

    def render_stats(self, surface, fps):
        ''' Render the player stats '''
        self.pos_label.render(surface, "X: " + str(int(self.pos.x)) + " | Y: "+str(int(self.pos.y)), 5, 30)
        self.fps_label.render(surface, "FPS: " + str(fps), 5, 50)
        self.fuel_label.render(surface, "Fuel: "+str(int(self.fuel)), self.fuel_pos[0], self.fuel_pos[1])
        self.score_label.render(surface, "Score: "+str(self.score), 5, 70)
        if self.fuel > 0:
            pygame.draw.line(surface, (0, 255, 0), (self.fuel_pos[0]+100, self.fuel_pos[1]+10), (self.fuel_pos[0]+100+self.fuel_length, self.fuel_pos[1]+10))

    def render(self, surface, cam):
        '''
            Render itself, the emitter and bullets.
        '''
        self.group.draw(surface)

        self.emitter.render(surface, cam)

        # Bullets
        for bullet in self.bullets:
            bullet.render(surface, cam)


    def update(self, delta, collision):
        if self.remove:
            self.score -= 1
            self.reset_pos()
            self.remove = False

        self.input(delta, collision)
        self.fuel_length = self.fuel*self.fuel_multiplier

        self.angle = self.angle % 360

        # Scale and rotate image based on angle
        self.rotate_fix()

        # Set vel from angle
        util.set_vel(self.vel, self.angle)

        # Fueling
        if self.on_pad and self.thrust == 0:
            self.fuel = util.lerp(self.fuel, config.max_fuel+1, delta)
            if self.angle > 345:
                self.angle = util.lerp(self.angle, 360, delta)
            else: self.angle = util.lerp(self.angle, 0, delta)
        else:
            self.on_pad = False
            # Apply speed and gravity
            x = self.thrust*self.vel.x*delta
            y = self.gravity*delta+self.thrust*self.vel.y*delta
            self.distance_traveled += abs(x+y)
            self.pos.x += x
            self.pos.y += y

            # Camera
            self.cam.x -= x
            self.cam.y -= y


        # Update sprite position
        self.sprite.rect.centerx = self.pos.x
        self.sprite.rect.centery = self.pos.y

        self.emitter.update(delta)
        # Update bullets
        for bullet in self.bullets:
            if bullet.remove:
                self.bullets.remove(bullet)
                continue
            bullet.update(delta)

    def apply_cam(self, cam):
        self.sprite.rect.center += cam

    def input(self, delta, collision):
        key = pygame.key.get_pressed()
        # Rotate left
        if key[self.left]:
            self.angle += delta*config.rotate_speed

        # Rotate right
        if key[self.right]:
            self.angle -= delta*config.rotate_speed

        # Thrust
        if key[self.up]:
            if self.fuel > 0:
                self.fuel -= config.fuel_consume*delta
                #self.fuel_length -= config.fuel_consume*delta
                self.thrust = config.thrust_power
                if self._p_timer >= self.p_add_time:
                    self.emitter.add(10, self.pos.x-self.vel.x*self.size[0]/2, self.pos.y-self.vel.y*self.size[1]/2, 10, 10)
                    self._p_timer = 0.0
                else: self._p_timer += delta
            elif self.vel.y > 0:
                self.thrust = config.thrust_power/2
            else: self.thrust = 0
        else: self.thrust = 0

        # Fire
        if key[self.fire]:
            if self._timer <= 0.0:
                self.bullets_fired += 1
                bullet = Bullet(self, util.bullet)
                self.bullets.append(bullet)
                collision.add_dynamic(bullet)
                self._timer = self.bullet_cooldown
        self._timer -= delta

    def get_controls(self, controls):
        c = controls.get(self.player)
        if c is not None:
            self.up = c.get("thrust")
            self.fire = c.get("fire")
            self.left = c.get("r_l")
            self.right = c.get("r_r")
        else: self.use_default()


    def use_default(self):
        if self.player == 1:
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.up = pygame.K_w
            self.fire = pygame.K_LCTRL
        elif self.player == 2:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.up = pygame.K_UP
            self.fire = pygame.K_RETURN
        else:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.up = pygame.K_UP
            self.fire = pygame.K_TAB

    def translate(self, pos):
        self.pos += pos
        self.sprite.center = self.pos
        self.cam -= pos

class Background(Entity):
    def __init__(self):
        super().__init__()

        self.emitter = emitter.Emitter()
        self.emitter.add_stars(200, config.map_size[0], config.map_size[1])
    def render(self, surface, cam):
        self.emitter.render(surface, cam)

    def update(self, delta):
        self.emitter.update_stars(delta)


class Mayhem(pygame.sprite.Sprite):
    def __init__(self, surface, controls):
        pygame.sprite.Sprite.__init__(self)
        self.id = "game"
        self.done = False
        self.sprite_group = pygame.sprite.Group()
        self.entity = []
        self.surfaces = []
        self.players = []
        self.collision = Collision()
        self.background = Background()

        # Time variables
        self.time = config.play_time
        self.clock_label = text.Label('Ariel', 25)
        self.clock_label.set_color((255, 255, 0))

        # Setting each player surfaces
        width = int(config.screen_size[0]/config.players)
        height = int(config.screen_size[1])
        x = 0
        for i in range(0, config.players):
            rect = pygame.Rect(x, 0, width, height)
            screen = surface.subsurface(rect)
            self.surfaces.append(screen)

            player = Player(util.player1, i+1, Vector2(width, height), controls)
            player.translate(Vector2(x, 0))
            self.sprite_group.add(player)

            self.entity.append(player)
            self.players.append(player)
            self.collision.add_dynamic(player)
            x += width

        # Add objects to lists provided
        self.map = Map(self.sprite_group, self.collision, self.entity)


        # Adding landing pad to players
        # to reset on when dead
        pads = []
        x = 0
        for i in self.players:
            i.landing_pads = self.map.landing_pads
            pads.append(self.map.landing_pads[x])
            x += 1

        for i in self.players:
            pads.remove(i.set_pos(pads))



    def render(self, surface, fps):
        ''' Render everything to each player surface,
            then blit each subsurface to main surface
        '''

        pos = 0
        offset = int(config.screen_size[0]/config.players)
        x = 0
        for screen, player in zip(self.surfaces, self.players):

            # Render background
            self.background.render(screen, player.cam)

            for ent in self.entity:
                # Apply cam position before rendering
                ent.apply_cam(player.cam)
                ent.render(screen, player.cam)
                ent.apply_cam(-player.cam)

            self.map.render(screen, player.cam)
            # Player stat rendering
            player.render_stats(screen, fps)

            # Debug
            if config.debug:
                self.collision.debug(screen, player.cam)

            if surface.get_locked():
                surface.blit(screen, (0, 0))

            # ~ Screen Divide start ~ #
            if x <= len(self.surfaces)-2:
                pos += offset
                pygame.draw.line(surface, config.divide_color, (pos, 0), (pos, config.screen_size[1]), config.divide_width)
                x += 1
            # ~ Screen Divide end ~ #

        txt = "Time left: "+str(int(self.time))
        self.clock_label.render(surface, txt, int(config.screen_size[0]/2-self.clock_label.get_size(txt)[0]/2), 5)

    def update(self, delta):
        if self.time <= 0:
            self.done = True
        else: self.time -= delta

        self.sprite_group.update(delta, self.collision)

        self.collision.update()
        self.background.update(delta)



# S
