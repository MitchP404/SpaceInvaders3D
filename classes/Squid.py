# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:02:49 2023

@author: mitch
"""

from classes.Enemy import Enemy
import os

class Squid(Enemy):
    def __init__(self, pos):
        Enemy.__init__(
                self,
                scale=(0.5, 0.5, 0.5),
                move=pos, 
                texFilepath=os.path.join("enemies", "squid.png"),
                points=30, 
                moveUpdate=[0.5, -0.02, 0.0], 
                shoots=90
            )