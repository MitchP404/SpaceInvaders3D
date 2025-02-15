import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time
import random
import math
import os

from classes.Cube import Cube
from classes.Player import Player
from classes.Barrier import Barrier
from classes.Enemy import Enemy
from classes.Octopus import Octopus
from classes.Crab import Crab
from classes.Squid import Squid
    
pygame.init()
pygame.display.set_caption("Space Invaders 3D")
clock = pygame.time.Clock()    

def makeWall(x, z):
    return Cube(
            scale = (z + 1.0, 2.0, x + 1.0),
            move = (x, 0, z),
            texFilepath = os.path.join("barrier", "barrier3.png"),
            paintOnAll = True
        )

# def addNewEnemy(typeOf, enemies):
#     if(typeOf == "octopus"):
#         Octopus([random()])

def game_loop():
    gameExit = False
    print("Inside game_loop")
    
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.5, 110.0)
    
    score = 0;
    wave = 1;
    
    #Enemy list
    enemies = [
            # Enemy(
            #         scale=(1.0, 1.0, 1.0), 
            #         move = [0.0, 40.0, 0.0], 
            #         texFilepath = os.path.join("enemies", "crab.png"), 
            #         points = 10, 
            #         moveUpdate = [-0.5, 0.0, 0.5], 
            #         shoots = True
            #     ),
            Octopus([-5.0, 20.0, 3.0]),
            Octopus([-3.0, 20.0, 3.0]),
            Octopus([-1.0, 20.0, 3.0]),
            Octopus([1.0, 20.0, 3.0]),
            Octopus([3.0, 20.0, 3.0]),
            Octopus([5.0, 20.0, 3.0]),
            Octopus([-5.0, 20.0, -3.0]),
            Octopus([-3.0, 20.0, -3.0]),
            Octopus([-1.0, 20.0, -3.0]),
            Octopus([1.0, 20.0, -3.0]),
            Octopus([3.0, 20.0, -3.0]),
            Octopus([5.0, 20.0, -3.0]),
            
            Octopus([-5.0, 25.0, 5.0]),
            Octopus([-3.0, 25.0, 5.0]),
            Octopus([-1.0, 25.0, 5.0]),
            Octopus([1.0, 25.0, 5.0]),
            Octopus([3.0, 25.0, 5.0]),
            Octopus([5.0, 25.0, 5.0]),
            Octopus([-5.0, 25.0, -5.0]),
            Octopus([-3.0, 25.0, -5.0]),
            Octopus([-1.0, 25.0, -5.0]),
            Octopus([1.0, 25.0, -5.0]),
            Octopus([3.0, 25.0, -5.0]),
            Octopus([5.0, 25.0, -5.0]),
            
            Crab([-5.0, 30.0, 3.0]),
            Crab([-3.0, 30.0, 3.0]),
            Crab([-1.0, 30.0, 3.0]),
            Crab([1.0, 30.0, 3.0]),
            Crab([3.0, 30.0, 3.0]),
            Crab([5.0, 30.0, 3.0]),
            Crab([-5.0, 30.0, -3.0]),
            Crab([-3.0, 30.0, -3.0]),
            Crab([-1.0, 30.0, -3.0]),
            Crab([1.0, 30.0, -3.0]),
            Crab([3.0, 30.0, -3.0]),
            Crab([5.0, 30.0, -3.0]),
            
            Crab([-5.0, 35.0, 5.0]),
            Crab([-3.0, 35.0, 5.0]),
            Crab([-1.0, 35.0, 5.0]),
            Crab([1.0, 35.0, 5.0]),
            Crab([3.0, 35.0, 5.0]),
            Crab([5.0, 35.0, 5.0]),
            Crab([-5.0, 35.0, -5.0]),
            Crab([-3.0, 35.0, -5.0]),
            Crab([-1.0, 35.0, -5.0]),
            Crab([1.0, 35.0, -5.0]),
            Crab([3.0, 35.0, -5.0]),
            Crab([5.0, 35.0, -5.0]),
            
            Squid([-5.0, 40.0, 3.0]),
            Squid([-3.0, 40.0, 3.0]),
            Squid([-1.0, 40.0, 3.0]),
            Squid([1.0, 40.0, 3.0]),
            Squid([3.0, 40.0, 3.0]),
            Squid([5.0, 40.0, 3.0]),
            Squid([-5.0, 40.0, -3.0]),
            Squid([-3.0, 40.0, -3.0]),
            Squid([-1.0, 40.0, -3.0]),
            Squid([1.0, 40.0, -3.0]),
            Squid([3.0, 40.0, -3.0]),
            Squid([5.0, 40.0, -3.0]),
            
            Squid([-5.0, 45.0, 5.0]),
            Squid([-3.0, 45.0, 5.0]),
            Squid([-1.0, 45.0, 5.0]),
            Squid([1.0, 45.0, 5.0]),
            Squid([3.0, 45.0, 5.0]),
            Squid([5.0, 45.0, 5.0]),
            Squid([-5.0, 45.0, -5.0]),
            Squid([-3.0, 45.0, -5.0]),
            Squid([-1.0, 45.0, -5.0]),
            Squid([1.0, 45.0, -5.0]),
            Squid([3.0, 45.0, -5.0]),
            Squid([5.0, 45.0, -5.0]),
        ]
    
    #Barrier list
    barriers = [
            Barrier(3.0,3.0),
            Barrier(5.0,3.0),
            Barrier(3.0,5.0),
            Barrier(5.0,5.0),
            
            Barrier(-3.0,3.0),
            Barrier(-5.0,3.0),
            Barrier(-3.0,5.0),
            Barrier(-5.0,5.0),
            
            Barrier(3.0,-3.0),
            Barrier(5.0,-3.0),
            Barrier(3.0,-5.0),
            Barrier(5.0,-5.0),
            
            Barrier(-3.0,-3.0),
            Barrier(-5.0,-3.0),
            Barrier(-3.0,-5.0),
            Barrier(-5.0,-5.0),
        ]
    
    player = Player()
    playerProjectile = None
    
    skybox = Cube(
            scale = (50.0, 50.0, 50.0),
            move = (0.0, 0.0, 0.0),
            texFilepath = "space.png",
            paintOnAll = True
        )
    
    boundaryBox = Cube(
            scale=(7.0, 25.0, 7.0),
            move=(0.0, 25.0, 0.0)
        )
    
    #Walls that are drawn to show where the player cannot leave
    walls = (
            makeWall(-8, 0),
            makeWall(8, 0),
            makeWall(0, -8),
            makeWall(0, 8)
        )
    
    glEnable(GL_DEPTH_TEST)
    
    gameOver = False
    
    while not gameExit:
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if(not gameOver):
                player.checkMove(event)
                if playerProjectile is None:
                    tempPlayerProjectile = player.checkShoot(event)
                    if(tempPlayerProjectile is not None):
                       playerProjectile = tempPlayerProjectile
            
        player.updateMove(boundaryBox)
        
        for enemy in enemies:
            if enemy.updateMove(boundaryBox):
                gameOver = True
        
        #Player projectile code
        if(playerProjectile is not None):
            playerProjectile.update()
            if(playerProjectile.getHighYBound() >= boundaryBox.getHighYBound()):
                playerProjectile = None
        
        #Barrier collision
        if(playerProjectile is not None):
            for barrier in barriers:
                if playerProjectile.cubeCollisionCheck(barrier):
                    playerProjectile = None
                    if(barrier.damage()):
                        barriers.remove(barrier)
                    break;
            
        #Enemy collision
        if(playerProjectile is not None):
            for enemy in enemies:
                if playerProjectile.cubeCollisionCheck(enemy):
                    print(enemy.destroy())
                    enemies.remove(enemy)
                    playerProjectile = None
                    break;
        
        #Get ready to draw
        #glEnable(GL_CULL_FACE);
        # do not draw back faces
        #glCullFace(GL_FRONT);
        glPushMatrix()
        player.cameraSet()
        
        #Draw the thingies
        
        #Skybox
        # faces are defined clock-wise
        glFrontFace(GL_CW);
        skybox.setupDraw()
        skybox.draw()
        # all other faces are defined counter-clock-wise
        glFrontFace(GL_CCW);
        
        #Walls
        for wall in walls:
            wall.setupDraw()
            wall.draw()
        
        #Barriers
        for barrier in barriers:
            barrier.setupDraw()
            barrier.draw()
            
        #Enemies
        for enemy in enemies:
            enemy.setupDraw()
            enemy.draw()
        
        #Player projectile
        if(playerProjectile is not None):
            playerProjectile.setupDrawColor()
            playerProjectile.drawColor()
        
        #Text
        if(gameOver):
            gameOverCube = Cube(
                    scale=(1.0, 1.0, 1.0), 
                    move=[player.move[0], player.move[1] + 3, player.move[2]], 
                    texFilepath = "GameOver.png", 
                    paintOnAll = False
                )
            gameOverCube.setupDraw()
            gameOverCube.draw()
        
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(60)

game_loop()
pygame.quit()


