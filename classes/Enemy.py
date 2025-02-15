# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 19:52:11 2023

@author: mitch
"""

from classes.Cube import Cube

class Enemy(Cube):
    
    def __init__(self, scale, move, texFilepath, points, moveUpdate, shoots):
        """
        Create a new enemy

        Parameters
        ----------
        scale : list
            The size of the enemy.
        move : list
            The starting position of the enemy.
        texFilepath : string
            The location of this enemy's texture.
        points : int
            How many points this enemy gives when destroyed.
        moveUpdate : list
            An xyz list containing a vector that gives a direction the enemy should travel in.
        shoots : int
            How many frames should go by between this enemy firing a shot. If -1, will not fire

        Returns
        -------
        The new cube.
        """
        Cube.__init__(
            self,
            scale=scale, 
            move=move, 
            texFilepath = texFilepath, 
            paintOnAll = False
            )
        self.points = points
        self.moveUpdate = moveUpdate
        self.shoots = shoots
    
    def updateMove(self, boundaryBox):
        """Move this enemy and see if it should bounce off of the walls of the boundaryBox"""
        for i in range(len(self.move)):
            self.move[i] += self.moveUpdate[i]
            
        diff = self.getHighXBound() - boundaryBox.getHighXBound()
        if diff > 0:
            self.move[0] -= diff
            self.moveUpdate[0] *= -1
        diff = self.getHighYBound() - boundaryBox.getHighYBound()
        if diff > 0:
            self.move[1] -= diff
            self.moveUpdate[1] *= -1
        diff = self.getHighZBound() - boundaryBox.getHighZBound()
        if diff > 0:
            self.move[2] -= diff
            self.moveUpdate[2] *= -1
            
        diff = self.getLowXBound() - boundaryBox.getLowXBound()
        if diff < 0:
            self.move[0] -= diff
            self.moveUpdate[0] *= -1
        diff = self.getLowYBound() - boundaryBox.getLowYBound()
        if diff < 0:
            self.move[1] -= diff
            self.moveUpdate[1] *= -1
            return True
        diff = self.getLowZBound() - boundaryBox.getLowZBound()
        if diff < 0:
            self.move[2] -= diff
            self.moveUpdate[2] *= -1
        return False;
        
    def destroy(self):
        return self.points
        