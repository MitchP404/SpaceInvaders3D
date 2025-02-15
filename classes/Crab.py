# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:55:57 2023

@author: mitch
"""

from classes.Enemy import Enemy
import os

class Crab(Enemy):
    def __init__(self, pos):
        Enemy.__init__(
                self,
                scale=(0.75, 0.75, 0.75),
                move=pos, 
                texFilepath=os.path.join("enemies", "crab.png"),
                points=20, 
                moveUpdate=[0.0, -0.02, 0.3], 
                shoots=120
            )