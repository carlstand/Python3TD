import pygame
import objects
import vector2
import math_extended
import GIFImage
import config

from config import *
from threading import Thread

from pygame.locals import *
from sys import exit
from random import *
from objects import *
from vector2 import *
from math_extended import *

waittime = 40
background_image_filename = 'pictures/Bikini-Bottom.jpg'
circle_filename = 'circle.gif'
lose_filename = 'pictures/lose.jpg'
SpongeBob_image_filenames = ['SpongeBob.gif', 'SpongeBob2.gif', 'SpongeBob3.gif']
Patrick_image_filenames = ['patrick.gif', 'patrick2.gif', 'patrick3.gif']
soundlist = ['sounds/ich_bin_bereit.ogg', '', 'sounds/ich_bin_nicht_bereit.ogg']

MAX_LOST = 3
max_of_defender = 30
max_of_producer = 20
no_of_hamburger = 0
spongebob_needs_hamb = 1
patrick_needs_hamb = 2
enmey_repro_speed = 3000
hamburger_repro_speed = 5000
level = 1

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Spongebob vs. Quallen")
background = pygame.image.load(background_image_filename).convert()
character1 = pygame.image.load(SpongeBob_image_filenames[0])
character1 = pygame.transform.scale(character1, (int(character1.get_width() / 2), int(character1.get_height() / 2)))
character2 = pygame.image.load(Patrick_image_filenames[0])
character2 = pygame.transform.scale(character2, (int(character2.get_width() / 2), int(character2.get_height() / 2)))
character1.set_alpha(128)
character2.set_alpha(128)
circle_producer = pygame.image.load(circle_filename).convert()
circle_producer = pygame.transform.scale(circle_producer, (detect_radius, detect_radius))
circle_producer.set_alpha(64)
circle_defender = circle_producer.copy()
circle_defender = pygame.transform.scale(circle_producer, character1.get_size())
font = pygame.font.SysFont("DejaVu Sans", 32);

hamburger = pygame.image.load('Hamburger.gif').convert()
hamburger = pygame.transform.scale(hamburger, (50, 50))
hamburger.set_alpha(128)
hamburger_pos = (0, 0)
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT + 1, enmey_repro_speed)
pygame.time.set_timer(USEREVENT + 2, hamburger_repro_speed)
selected1 = False
selected2 = False

# container
allbullet = pygame.sprite.Group()
allbox = pygame.sprite.Group()
alldefender = pygame.sprite.Group()
allproducer = pygame.sprite.Group()
allhamburger = pygame.sprite.Group()
lost = 0


def mainthread():
    global max_of_defender, max_of_producer, no_of_hamburger, spongebob_needs_hamb, patrick_needs_hamb, enmey_repro_speed, hamburger_repro_speed
    global no_of_hamburger, selected1, selected2, lost, level
    global allbullet, allbox, alldefender, allproducer, allhamburger

    while True:

        no_of_defender = no_of_hamburger / spongebob_needs_hamb
        no_of_producer = no_of_hamburger / patrick_needs_hamb
        # print lost
        screen.blit(background, (0, 0))

        # display passed time at right-upper
        timetext = str(pygame.time.get_ticks() / 1000) + ' seconds'
        font_width, font_height = font.size(timetext)
        rendered_font = font.render(timetext, True, (0, 0, 255))
        screen.blit(rendered_font, (SCREEN_SIZE[0] - font_width, 0))

        # display no_of_hamburger at left-upper
        hamburger.set_alpha(128)
        screen.blit(hamburger, (0, 0))
        hamburgertext = ' x ' + str(no_of_hamburger)
        font_width, font_height = font.size(hamburgertext)
        rendered_font = font.render(hamburgertext, True, (255, 0, 255))
        screen.blit(rendered_font, (hamburger.get_width(), 0))

        # display spongebob at right-bottom
        character1_pos = (screen.get_width() - character1.get_width(), SCREEN_SIZE[1] - character1.get_height())
        screen.blit(character1, (character1_pos))
        spongebobtext = str(len(alldefender)) + ' x '
        font_width, font_height = font.size(spongebobtext)
        rendered_font = font.render(spongebobtext, True, (255, 0, 255))
        screen.blit(rendered_font, (SCREEN_SIZE[0] - character1.get_width() - font_width, SCREEN_SIZE[1] - font_height))
        hamburger.set_alpha(128)
        screen.blit(hamburger, (SCREEN_SIZE[0] - character1.get_width() - hamburger.get_width(), \
                                SCREEN_SIZE[1] - font_height - hamburger.get_height()))

        # display patrick at left-bottom
        character2_pos = Vector2(0, screen.get_height() - character2.get_height())
        screen.blit(character2, Vector2.as_tuple(character2_pos))
        patricktext = ' x ' + str(len(allproducer))
        font_width, font_height = font.size(patricktext)
        rendered_font = font.render(patricktext, True, (255, 0, 255))
        screen.blit(rendered_font, (character2.get_width(), SCREEN_SIZE[1] - font_height))
        hamburger.set_alpha(128)
        screen.blit(hamburger, (character2.get_width(), \
                                SCREEN_SIZE[1] - font_height - hamburger.get_height()))
        screen.blit(hamburger, (character2.get_width() + hamburger.get_width(), \
                                SCREEN_SIZE[1] - font_height - hamburger.get_height()))

        # if mouse over characters then emphasize them
        mouse_pos = pygame.mouse.get_pos()
        in_character1 = inrect(((character1_pos), character1.get_size()), mouse_pos)
        if in_character1:
            character1.set_alpha(255)
        else:
            character1.set_alpha(128)

        in_character2 = inrect(((character2_pos), character2.get_size()), mouse_pos)
        if in_character2:
            character2.set_alpha(255)
        else:
            character2.set_alpha(128)

            # event list processing
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONUP:
                if event.button == 3:
                    selected1 = False
                    selected2 = False
                if event.button == 1:
                    if (selected1 or selected2) and not in_character1 and not in_character2:
                        object.rect.center = pygame.mouse.get_pos()
                        group.add(object)
                        if selected1:
                            selected1 = False
                            no_of_hamburger -= spongebob_needs_hamb
                        elif selected2:
                            selected2 = False
                            no_of_hamburger -= patrick_needs_hamb
                        if no_of_hamburger < 0:
                            no_of_hamburger = 0
                    elif in_character1:
                        if no_of_hamburger >= spongebob_needs_hamb:
                            imagelist = SpongeBob_image_filenames
                            defender_image = GIFImage.GIFImage(imagelist[0])
                            group = alldefender
                            object = Defender(screen, imagelist, soundlist)
                            selected1 = True
                    elif in_character2:
                        if no_of_hamburger >= patrick_needs_hamb:
                            imagelist = Patrick_image_filenames
                            defender_image = GIFImage.GIFImage(imagelist[0])
                            group = allproducer
                            object = Producer(screen, imagelist, soundlist)
                            selected2 = True
                    else:
                        for ham in allhamburger:
                            if inrect((ham.pos, (70, 70)), mouse_pos):
                                ham.kill()
                                no_of_hamburger += 1
            if event.type == USEREVENT + 1:
                Enemy(allbox, screen)
            if event.type == USEREVENT + 2:
                Food(allhamburger, screen)
            if event.type == USEREVENT + 3:
                lost += event.code

        # set mouse cursor
        if selected1 or selected2:
            x, y = mouse_pos
            x -= defender_image.get_width() / 2
            y -= defender_image.get_height() / 2
            defender_image.render(screen, (x, y))

        # sprite update section
        allbullet.update()
        allbullet.draw(screen)

        alldefender.update()
        allproducer.update()

        allbox.update()

        allhamburger.update()
        allhamburger.draw(screen)

        # collide detection section
        # check the collide between bullets and enemies
        boxlist = pygame.sprite.groupcollide(allbox, allbullet, False, True)
        if len(boxlist):
            for box in boxlist:
                bulletslist = boxlist[box]
                for bullet in bulletslist:
                    box.get_damage += bullet.damage

                    # check the collide between enemies and defenders
        defenderlist = pygame.sprite.groupcollide(alldefender, allbox, False, True)
        if len(defenderlist):
            for defender in defenderlist:
                boxlist = defenderlist[defender]
                for box in boxlist:
                    defender.get_damage += box.damage

                    # check the collide between enemies and defenders
        list = pygame.sprite.groupcollide(allproducer, allbox, False, True)
        if len(list):
            for defender in list:
                boxlist = list[defender]
                for box in boxlist:
                    defender.get_damage += box.damage

                    # if defenders find enmey then fire
        for defender in alldefender:
            defender.fire(allbox)
            allbullet.add(defender.bulletgroup)

        for producer in allproducer:
            for defender in alldefender:
                dis = Vector2.from_points(defender.rect.center, producer.rect.center)
                if dis.get_length() < detect_radius / 2:
                    producer.support_group.add(defender)

        if selected1:
            for producer in allproducer:
                dis = Vector2.from_points(mouse_pos, producer.rect.center)
                if dis.get_length() < detect_radius / 2:
                    circle_producer.set_alpha(64)
                    x = producer.rect.center[0] - circle_producer.get_width() / 2
                    y = producer.rect.center[1] - circle_producer.get_height() / 2
                    screen.blit(circle_producer, (x, y))

                else:
                    circle_producer.set_alpha(0)

        if selected2:
            circle_producer.set_alpha(64)
            x = mouse_pos[0] - circle_producer.get_width() / 2
            y = mouse_pos[1] - circle_producer.get_height() / 2
            screen.blit(circle_producer, (x, y))
            for defender in alldefender:
                dis = Vector2.from_points(mouse_pos, defender.rect.center)
                if dis.get_length() < detect_radius / 2:
                    circle_defender.set_alpha(64)
                    x = defender.rect.center[0] - circle_defender.get_width() / 2
                    y = defender.rect.center[1] - circle_defender.get_height() / 2
                    screen.blit(circle_defender, (x, y))

            for producer in allproducer:
                circle_producer.set_alpha(64)
                x = producer.rect.center[0] - circle_producer.get_width() / 2
                y = producer.rect.center[1] - circle_producer.get_height() / 2
                screen.blit(circle_producer, (x, y))

        else:
            circle_producer.set_alpha(0)
            circle_defender.set_alpha(0)

        if lost >= MAX_LOST:
            break

        time_passed = pygame.time.get_ticks() / 1000
        if time_passed > level * 5:
            level += 1
            print(level)
            enmey_repro_speed -= 100
            if enmey_repro_speed < 500:
                enmey_repro_speed = 500
            print (enmey_repro_speed)
            pygame.time.set_timer(USEREVENT + 1, enmey_repro_speed)
            #    if time_passed > 20:
            #        break
        pygame.time.wait(waittime)
        pygame.display.update()


def waitforexit():
    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
        pygame.time.wait(waittime)


def main():
    ##    mthread = Thread(None, mainthread, None)
    ##    mthread.start()
    ##    mthread.join()
    mainthread()

    background.set_alpha(128)
    screen.blit(background, (0, 0))
    font = pygame.font.SysFont("DejaVu Sans", 50);
    font.set_bold(True)
    if lost >= MAX_LOST:
        finaltext = 'your time is: ' + str(pygame.time.get_ticks() / 1000) + ' s'
    else:
        finaltext = 'you win!!!'
    font_width, font_height = font.size(finaltext)
    rendered_font = font.render(finaltext, True, (0, 255, 255))
    screen.blit(rendered_font, ((SCREEN_SIZE[0] - font_width) / 2, (SCREEN_SIZE[1] - font_height) / 2))
    pygame.display.update()

    waitforexit()


##    exitthread = Thread(None, waitforexit, None)
##    exitthread.start()
##    exitthread.join()

if __name__ == '__main__': main()
