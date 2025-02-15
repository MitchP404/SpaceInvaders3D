# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:31:07 2023

Class that defines a cube object

@author: mitch
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
import os

class Cube:
    """A class representing a cube"""
    
    verticies = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )
    """The verticies of a cube without transformations"""
    
    edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7)
    )
    """Which vertecies make up the edges of a cube"""
    
    surfaces = (
        (0,1,2,3),
        (3,2,7,6),
        (6,7,5,4),
        (4,5,1,0),
        (1,5,7,2),
        (6,4,0,3)
    )
    """Which verticies make up each surface of the cube"""
    
    uvData = (
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1)    
    )
    """The UV coordinate data of each face"""
    
    @staticmethod
    def uploadTexture(file):
        """Take in a texture's filepath and return the image object, datastring, and texture id"""
        # read image specified by file name (here - local directory)
        # will create a new surface object from data. 
        image = pygame.image.load(os.path.join("textures", file))
        # creates a string of bytes, format needed by glTexImage2D
        data = pygame.image.tostring(image, 'RGBA')
        return (image, data, glGenTextures(1))
    
    def __init__(self, scale, move, texFilepath = None, paintOnAll = None, color = None):
        """
        Create a new cube object

        Parameters
        ----------
        scale : list
            An x, y, z list represting the scale on all axes.
        move : list
            An x, y, z list representing the movement on all axes.
        texFilepath : String
            The file where this cubes texture is stored
        paintOnAll : bool
            Whether or not the texture should be placed on all sides or just the bottom one
        
        Returns
        -------
        The new cube.

        """
        self.scale = scale
        self.move = move
        if(texFilepath is not None and paintOnAll is not None):
            imageInfo = Cube.uploadTexture(texFilepath)
            self.textureImage = imageInfo[0]
            self.textureData = imageInfo[1]
            self.textureID = imageInfo[2]
        if(paintOnAll is not None):
            self.paintOnAll = paintOnAll
        if(color is not None):
            self.color = color
    
    #Functions that return the x,y,z bounds of this object
    def getHighXBound(self):
        return self.move[0] + self.scale[0]
    def getLowXBound(self):
        return self.move[0] - self.scale[0]
    def getHighYBound(self):
        return self.move[1] + self.scale[1]
    def getLowYBound(self):
        return self.move[1] - self.scale[1]
    def getHighZBound(self):
        return self.move[2] + self.scale[2]
    def getLowZBound(self):
        return self.move[2] - self.scale[2]
    
    
    
    def setupDraw(self):
        """Has open gl create the modelview matrix for drawing this object and set up the texture
        """
        glPushMatrix()
        glTranslatef(self.move[0], self.move[1], self.move[2])
        glScalef(self.scale[0], self.scale[1], self.scale[2])
        
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glTexImage2D(
            GL_TEXTURE_2D, # The target texture for definition
            0, # Level of detail. Used for mipmapping.
            GL_RGBA, # What color components are in the texture
            self.textureImage.get_width(), # Width of the texture
            self.textureImage.get_height(), # Height of the texture
            0, # The wiki genuinely says "This value must be 0". WHY IS IT HERE XD
            GL_RGBA, # The format of the pixel data.
            GL_UNSIGNED_BYTE, # The data type of the pixel data
            self.textureData # A pointer to the image data in memory
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glEnable(GL_TEXTURE_2D)
    
    def setupDrawColor(self):
        glPushMatrix()
        glTranslatef(self.move[0], self.move[1], self.move[2])
        glScalef(self.scale[0], self.scale[1], self.scale[2])
    
    def draw(self):
        """Draw the object then pop its matrix"""
        glBegin(GL_QUADS)
        if(self.paintOnAll == True):
            for surface in Cube.surfaces:
                uvCoordIndex = 0
                for vertex in surface:
                    glTexCoord2fv(Cube.uvData[uvCoordIndex])
                    glVertex3fv(Cube.verticies[vertex])
                    uvCoordIndex += 1
        else:
            uvCoordIndex = 0
            for vertex in Cube.surfaces[5]:
                glTexCoord2fv(Cube.uvData[uvCoordIndex])
                glVertex3fv(Cube.verticies[vertex])
                uvCoordIndex += 1
        glEnd()
        
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        
    def drawColor(self):
        glBegin(GL_QUADS)
        for surface in Cube.surfaces:
            for vertex in surface:
                glColor3fv(self.color)
                glVertex3fv(Cube.verticies[vertex])
        glEnd()
        
        # glBegin(GL_LINES)
        # for edge in Cube.edges:
        #     for vertex in edge:
        #         glVertex3fv(Cube.verticies[vertex])
        # glEnd()
        glPopMatrix()
        
    def cubeCollisionCheck(self, cubeB):
        """Checks if this cube and cubeB are colliding"""
        if(
                (
                    (self.getHighXBound() >= cubeB.getLowXBound() and self.getHighXBound() <= cubeB.getHighXBound()) or
                    (self.getLowXBound() <= cubeB.getHighXBound() and self.getLowXBound() >= cubeB.getLowXBound())
                 ) and
                (
                    (self.getHighYBound() >= cubeB.getLowYBound() and self.getHighYBound() <= cubeB.getHighYBound()) or 
                    (self.getLowYBound() <= cubeB.getHighYBound() and self.getLowYBound() >= cubeB.getLowYBound())
                 ) and 
                (
                    (self.getHighZBound() >= cubeB.getLowZBound() and self.getHighZBound() <= cubeB.getHighZBound()) or 
                    (self.getLowZBound() <= cubeB.getHighZBound() and self.getLowZBound() >= cubeB.getLowZBound())
                )
            ):
            return True
        return False
    
    # def cubeWithin(self, cubeB):
    #     """Checks if this cube is completely contained in cubeB"""
    #     if(
    #             self.getHighXBound() < cubeB.getHighXBound and
    #             self.getLowXBound() > cubeB.getLowXBound and
    #             self.getHighYBound() < cubeB.getHighYBound and
    #             self.getLowYBound() > cubeB.getLowYBound and
    #             self.getHighZBound() < cubeB.getHighZBound and
    #             self.getLowZBound() > cubeB.getLowZBound
    #         ):
    #         return True
    #     return False