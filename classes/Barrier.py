# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 04:00:23 2023

@author: mitch
"""

from classes.Cube import Cube
import os

class Barrier(Cube):
    
    def setActiveTexture(self, tex):
        self.textureImage = tex[0]
        self.textureData = tex[1]
        self.textureID = tex[2]
    
    def __init__(self, x, z):
        Cube.__init__(
                self,
                scale=(1.0, 1.0, 1.0),
                move=(x, 5.0, z),
                paintOnAll = True
            )
        self.tex1 = Cube.uploadTexture(os.path.join("barrier", "barrier1.png"))
        self.tex2 = Cube.uploadTexture(os.path.join("barrier", "barrier2.png"))
        self.tex3 = Cube.uploadTexture(os.path.join("barrier", "barrier3.png"))
        
        self.setActiveTexture(self.tex3)
        
        self.health = 3
        
    def damage(self):
        """Returns true if this should be destroyed"""
        self.health -= 1
        if(self.health == 2):
            self.setActiveTexture(self.tex2)
            return False
        elif(self.health == 1):
            self.setActiveTexture(self.tex1)
            return False
        elif(self.health == 0):
            return True