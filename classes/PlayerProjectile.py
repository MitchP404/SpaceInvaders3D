# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 03:31:02 2023

@author: mitch
"""

from classes.Cube import Cube
import os

class PlayerProjectile(Cube):
    def __init__(self, x, z):
        Cube.__init__(
            self,
            scale=(0.25,0.5,0.25), 
            move=[x, 0.5, z], 
            color=(1,1,1)
            # texFilepath = os.path.join("barrier", "barrier3.png"),
            # paintOnAll = True
        )
    
    def update(self):
        self.move[1] += 2.0
        # print(self.move[1])