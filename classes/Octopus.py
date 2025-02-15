# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:15:25 2023

@author: mitch
"""

from classes.Enemy import Enemy
import os

class Octopus(Enemy):
    def __init__(self, pos):
        Enemy.__init__(
                self,
                scale=(1.0, 1.0, 1.0),
                move=pos, 
                texFilepath=os.path.join("enemies", "octopus.png"),
                points=10, 
                moveUpdate=[-0.1, -0.02, -0.1], 
                shoots=-1
            )