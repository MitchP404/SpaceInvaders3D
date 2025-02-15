# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:47:12 2023

@author: mitch
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos, sqrt, pi
from random import randint

pygame.init()
gameDisplay = (1000,800)
pygame.display.set_mode(gameDisplay, DOUBLEBUF | OPENGL)
pygame.display.set_caption('First Person Shooting')
clock = pygame.time.Clock()

R = [   0, 255,   0, 255, 255,   0,   0, 128, 210]
G = [   0,   0, 255, 255,   0, 255, 191,   0, 105]
B = [ 255,   0,   0,   0, 255, 255, 255,   0,  30]

ground_vertices = (( 10, -1, 10),
                   (-10, -1, 10),
                   (-10, -1,-10),
                   ( 10, -1,-10)
                   )
ground_edges = ((0,1),
                (1,2),
                (2,3),
                (3,0))
ground_face = (0,1,2,3)
ground_texture_coords = ((1,1),
                         (1,0),
                         (0,0),
                         (0,1))
image = pygame.image.load('happy_birthday.jpg')
data = pygame.image.tostring(image,'RGBA')
texID = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texID)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glEnable(GL_TEXTURE_2D)
glEnable(GL_CULL_FACE)
glCullFace(GL_FRONT)
glFrontFace(GL_CCW)

def Ground():
    glBegin(GL_QUADS)
    
    for i,vertex in enumerate(ground_face):
        glTexCoord2fv(ground_texture_coords[i])
        glVertex3fv(ground_vertices[vertex])
        
    glEnd()

def update_display(eyex, eyey, eyez, lookat_x, lookat_y, lookat_z, upx, upy, upz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()
    gluLookAt(eyex, eyey, eyez, lookat_x, lookat_y, lookat_z, upx, upy, upz)
    Ground()
    glPopMatrix()
    pygame.display.flip()
    pygame.time.wait(60)

def game_loop():
    gameExit = False
    eyeX = 0
    eyeY = 0
    eyeZ = 0
    
    lookat_x = 0
    lookat_y = 0
    lookat_z = 0
    lookat_y_change = 0
    
    upx = 0
    upy = 1
    upz = 0
    
    hor_angle = 0
    hor_change = 0
    ver_angle = 0
    ver_change = 0
    angleDelta = 0.1
    
    gluPerspective(90, gameDisplay[0]/gameDisplay[1], 0.5, 50.0)
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hor_change = angleDelta
                elif event.key == pygame.K_LEFT:
                    hor_change = -angleDelta
                elif event.key == pygame.K_UP:
                    ver_change = angleDelta
                elif event.key == pygame.K_DOWN:
                    ver_change = -angleDelta
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    hor_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ver_change = 0
            
            #xz-plane using same horizontal change in theta
            hor_angle = (hor_angle + hor_change) % (2 * pi)
            lookat_x = cos(hor_angle)
            lookat_z = sin(hor_angle)
            
            #xy-plane using vertical change in beta
            ver_angle = (ver_angle + ver_change) % (2 * pi)
            lookat_y = sin(ver_angle)
            
            update_display(eyeX, eyeY, eyeZ, lookat_x, lookat_y, lookat_z, upx, upy, upz)
            
game_loop()
pygame.quit()












