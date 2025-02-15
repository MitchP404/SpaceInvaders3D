# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 00:28:20 2023

@author: mitch
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from classes.Cube import Cube
from classes.PlayerProjectile import PlayerProjectile

class Player(Cube):
    """A class representing the player object"""
    
    def __init__(self):
        """Create a new player object"""
        Cube.__init__(self, (0.5,0.5,0.5), [0.0, 0.0, 0.0])
        self.speed = 0.5
        self.xChange = 0.0
        self.zChange = 0.0
        self.upDir = (0.0, 0.0, 1.0)
    
    def checkMove(self, event):
        """Checks if this event should cause the player to do an event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.zChange = self.speed
            elif event.key == pygame.K_s:
                self.zChange = -self.speed
            elif event.key == pygame.K_d:
                self.xChange = self.speed
            elif event.key == pygame.K_a:
                self.xChange = -self.speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.zChange = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                self.xChange = 0
    
    def checkShoot(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Left mouse button clicked
                return PlayerProjectile(self.move[0], self.move[2])
    
    def updateMove(self, boundaryBox):
        self.move[0] += self.xChange
        self.move[2] += self.zChange
        
        diff = self.getHighXBound() - boundaryBox.getHighXBound()
        if diff > 0:
            self.move[0] -= diff
        diff = self.getHighYBound() - boundaryBox.getHighYBound()
        if diff > 0:
            self.move[1] -= diff
        diff = self.getHighZBound() - boundaryBox.getHighZBound()
        if diff > 0:
            self.move[2] -= diff
            
        diff = self.getLowXBound() - boundaryBox.getLowXBound()
        if diff < 0:
            self.move[0] -= diff
        diff = self.getLowYBound() - boundaryBox.getLowYBound()
        if diff < 0:
            self.move[1] -= diff
        diff = self.getLowZBound() - boundaryBox.getLowZBound()
        if diff < 0:
            self.move[2] -= diff
        
    def cameraSet(self):
        """Set the current gl matrix to a look at matrix based on this object"""
        gluLookAt(
                self.move[0], self.move[1], self.move[2], 
                self.move[0], self.move[1] + 1.0, self.move[2], 
                self.upDir[0], self.upDir[1], self.upDir[2]
            )