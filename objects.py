import config
from config import *

#images
bullet_image_filename = 'bullet1.png'
box_image_filename = 'pictures/jellyfish.gif'
hamburger_image_filename = 'Hamburger.gif'
#sounds
jellyfish_sound_filename = 'sounds/jellyfish.ogg'


stage1, stage2, stage3 = range(3)
bullet_speed = 200
bullet_damage = 30
number_of_bullets = 3

enemy_speed = 30 
enemy_blood = 120
enemy_damage = 90

defender_blood = 270

detect_radius = 400

max_fire_speed = 2000 #ms

import pygame
import vector2
import math_extended
import GIFImage

from pygame.locals import *
from sys import exit
from random import *
from math import *
from math_extended import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, screen, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.speed = bullet_speed
        #damage system
        self.damage = bullet_damage
        
        self.direction = direction
        self.pos = pos
        self.angle = angle_of_vector2(Vector2(0, -1), self.direction)
        if direction[0] > 0:
            self.angle *= -1
        self.image = pygame.image.load(bullet_image_filename).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, degrees(self.angle), 0.1)    

        self.rect = self.image.get_rect()
        self.rect.center = Vector2.as_tuple(self.pos)
        self.clock = pygame.time.Clock()
        
        group.add(self)
                        
    def update(self):
        self.position()
        self.rect.center = (self.pos.x, self.pos.y)
        self.checkBounds()

    def position(self):
        time_passed = self.clock.tick()/1000.0
        self.pos += self.direction*self.speed*time_passed

    def checkBounds(self):
        if self.pos.y < 0 or self.pos.y > self.screen.get_height() or \
           self.pos.x < 0 or self.pos.x > self.screen.get_width():
            self.kill()

class Food(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        self.image = pygame.image.load(hamburger_image_filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()
        self.rect.center = (randint(100, SCREEN_SIZE[0]), randint(200, SCREEN_SIZE[1]))
        self.pos = (self.rect.center[0]-35, self.rect.center[1]-35)
        
        self.clock = pygame.time.Clock()
        self.time = 0
        group.add(self)
                        
    def update(self):
        self.checkTime()

    def checkTime(self):
        self.time += self.clock.tick()/1000.0
        if self.time > 10:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image=GIFImage.GIFImage(box_image_filename, 192)
        #self.image.set_alpha(120)
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (randint(self.rect.width,self.screen.get_width()-self.rect.width), -50)
        self.speed = enemy_speed
        #damage system        
        self.damage = enemy_damage
        self.blood = enemy_blood
        self.get_damage = 0
        
        self.direction = Vector2(randint(-10, 10), randint(1, 10))
        self.direction.normalise()
        self.pos = Vector2(self.rect.center)
        self.clock = pygame.time.Clock()
        
        self.sound = pygame.mixer.Sound(jellyfish_sound_filename)
        self.sound.play()
        group.add(self)
        
    def update(self):
        self.image.render(self.screen, Vector2.as_tuple(Vector2(self.rect.center)-Vector2(self.size)*0.5))
        self.position()
        self.rect.center = (self.pos.x, self.pos.y)
        self.checkBounds()
        self.checkBlood()
    
    def position(self):
        time_passed = self.clock.tick()/1000.0
        self.pos += self.direction*self.speed*time_passed
        
    def checkBounds(self):
        if self.pos.y > self.screen.get_height():
            self.kill()
            e = pygame.event.Event(USEREVENT+3, {'code': 1})
            pygame.event.post(e)
            print ('you lose!')
        elif self.pos.x +self.rect.width/2 > self.screen.get_width() or self.pos.x -self.rect.width/2 < 0:
            self.direction.x *=-1
            
    def checkBlood(self):
        self.blood -= self.get_damage
        self.get_damage = 0
        if self.blood <= 0:
            self.kill()
            
class Friend(pygame.sprite.Sprite):
    def __init__(self, screen, imagelist, soundlist):
        pygame.sprite.Sprite.__init__(self)
        self.imagelist = imagelist
        self.screen = screen
        self.image = GIFImage.GIFImage(self.imagelist[0])
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.bulletgroup = pygame.sprite.Group()
        
        self.currentstate = stage1
        self.nextstate = stage1
        self.radius = detect_radius
        self.clock = pygame.time.Clock()
        #sum_of_time to check the time passed
        self.sum_of_time = 0
        #damage system
        self.blood = defender_blood
        self.get_damage = 0
        self.get_blood = 0
        
        self.startingsound = pygame.mixer.Sound(soundlist[0])
        self.stoppingsound = pygame.mixer.Sound(soundlist[2])
        self.startingsound.play()
        
    def update(self):
        self.image.render(self.screen, Vector2.as_tuple(Vector2(self.rect.center)-Vector2(self.size)*0.5))
        self.checkBlood()
        self.checkStage()
        
    def checkBlood(self):
        self.blood -= self.get_damage
        if self.blood <= 0:
            self.stoppingsound.play()
            self.kill()
        self.get_damage = 0
        
#        print self.get_blood
        self.blood += self.get_blood
        if self.blood > defender_blood:
            self.blood = defender_blood
        self.get_blood = 0
             
        
    def checkStage(self):
        if self.currentstate == stage1:
            if self.blood > 2*defender_blood/3:
                self.nextstate = stage1
            elif self.blood > defender_blood/3 and self.blood <= 2*defender_blood/3:
                self.nextstate = stage2
                self.image = GIFImage.GIFImage(self.imagelist[1])
            elif self.blood > 0 and self.blood <= defender_blood/3:
                self.nextstate = stage3
                self.image = GIFImage.GIFImage(self.imagelist[2])

        elif self.currentstate == stage2:
            if self.blood > 2*defender_blood/3:
                self.nextstate = stage1
                self.image = GIFImage.GIFImage(self.imagelist[0])
            elif self.blood > defender_blood/3 and self.blood <= 2*defender_blood/3:
                self.nextstate = stage2
            elif self.blood > 0 and self.blood <= defender_blood/3:
                self.nextstate = stage3
                self.image = GIFImage.GIFImage(self.imagelist[2])            
        
        elif self.currentstate == stage3:
            if self.blood > 2*defender_blood/3:
                self.nextstate = stage1
                self.image = GIFImage.GIFImage(self.imagelist[0])
            elif self.blood > defender_blood/3 and self.blood <= 2*defender_blood/3:
                self.nextstate = stage2
                self.image = GIFImage.GIFImage(self.imagelist[1]) 
            elif self.blood > 0 and self.blood <= defender_blood/3:
                self.nextstate = stage3
                
        self.currentstate = self.nextstate
        
class Defender(Friend):
    def __init__(self, screen, imagelist, soundlist):
        Friend.__init__(self, screen, imagelist, soundlist)
        
    def fire(self, allbox):
        #sum_of_time to control fire speed
        self.sum_of_time += self.clock.tick()
        
        #if time passed bigger than max_fire_speed then fire
        if self.sum_of_time > max_fire_speed:
            self.sum_of_time = 0
            boxlist = pygame.sprite.spritecollide(self, allbox, False, pygame.sprite.collide_circle)
            # if find enemy and fired bullets are less than 3
            if len(boxlist) and len(self.bulletgroup) < number_of_bullets:

                #find the nearest enemy
                length=detect_radius + max(self.size)
                for box in boxlist:
                    tempvector = Vector2.from_points(self.rect.center, box.rect.center)
                    if length > tempvector.get_length():
                        length=tempvector.get_length()
                        nearestbox=box
                
                #caculate the fire direction
                if nearestbox:
                    vec1 = Vector2.from_points(nearestbox.rect.center, self.rect.center)
                    vec2 = nearestbox.direction.copy()
                    dist = vec1.get_length()
                    angle = angle_of_vector2(vec1, vec2)
                    s = cos(angle)*dist
                    v1=bullet_speed
                    v2=enemy_speed
                    root=roots2(v2**2-v1**2, -2*s*(v2**2), (dist*v2)**2)
                    dest = Vector2(nearestbox.rect.center) + nearestbox.direction*nearest_zero(root)
                    
                    # set the property of bullets(direction, start position)
                    direction=Vector2.from_points(self.rect.center, dest)
                    direction.normalise()
                    pos = Vector2(self.rect.center)
                    self.bullet = Bullet(self.bulletgroup, self.screen, pos, direction)    

class Producer(Friend):
    def __init__(self, screen, imagelist, soundlist):
        Friend.__init__(self, screen, imagelist, soundlist)
        self.bloodup_speed = 10
        self.support_group = pygame.sprite.Group()
    
    def make_HP(self):
        time_passed = self.clock.tick()/1000.0
        added_blood = self.bloodup_speed*time_passed
        self.get_blood = added_blood / 10.0
        for element in self.support_group:
            element.get_blood += added_blood

    def update(self):
        Friend.update(self)
        self.make_HP()
