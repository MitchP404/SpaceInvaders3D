import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random
import math

pygame.init()
pygame.display.set_caption("Camera Fly")
clock = pygame.time.Clock()

ground_vertices =((10,-1,10),(-10,-1,10),(-10,-1,-10),(10,-1,-10))
ground_edges = ((0,1),(1,2),(2,3),(3,0))
ground_face = ((0,1,2,3))
ground_texture_coords = ((1,1),(1,0),(0,0),(0,1))

verticies = (
    (1, -1, -1), # 0
    (1, 1, -1), # 1
    (-1, 1, -1), # 2
    (-1, -1, -1), # 3
    (1, -1, 1), # 4
    (1, 1, 1), # 5
    (-1, -1, 1), # 6
    (-1, 1, 1) # 7
)

# Represents the uv data of each face
uvData = (
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)    
)

edges = (
    (0,1), # e0
    (0,3), # e1
    (0,4), # e2
    (2,1), # e3
    (2,3), # e4
    (2,7), # e5
    (6,3), # e6
    (6,4), # e7
    (6,7), # e8
    (5,1), # e9
    (5,4), # e10
    (5,7) # e11
    )

surfaces = (
    (0,1,2,3), # f0
    (3,2,7,6), # f1
    (6,7,5,4), # f2
    (4,5,1,0), # f3
    (1,5,7,2), # f4
    (4,0,3,6) # f5
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,1),
    (1,0,1),
    (1,1,0),
    )
 
def Cube(image, data, texID):
    
    # TEXTURING
    #Sets (or "binds") the current 2D texture to the texture name stored in texID
    glBindTexture(GL_TEXTURE_2D, texID)
    
    # Define a new texture image.
    #This line does a LOT and is easier to explain by saying what its parameters are
    #Basically, this allows the shader itself to map the image onto objects
    glTexImage2D(
        GL_TEXTURE_2D, # The target texture for definition
        0, # Level of detail. Used for mipmapping.
        GL_RGBA, # What color components are in the texture
        image.get_width(), # Width of the texture
        image.get_height(), # Height of the texture
        0, # The wiki genuinely says "This value must be 0". WHY IS IT HERE XD
        GL_RGBA, # The format of the pixel data.
        GL_UNSIGNED_BYTE, # The data type of the pixel data
        data # A pointer to the image data in memory
    )
    
    #Applies extra parameters to how the texture is drawn.
    #These two are for growing and shrinking the texture as needed
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    #Finally enable the stupid picture
    glEnable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS)
    for surface in surfaces:
        uvCoordIndex = 0
        for vertex in surface:
            glTexCoord2fv(uvData[uvCoordIndex])
            glVertex3fv(verticies[vertex])
            uvCoordIndex += 1
    glEnd()
    
    # glColor3fv((1,1,1))
    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(verticies[vertex])
    # glEnd()  

def update_display(eyex, eyey, eyez, cx, cy, cz, jump, image, data, texID):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # OpenGL checks all the faces that are front facing towards the viewer 
    # and renders those, while discarding all the faces that are back facing
    # think: how many faces you can see in the cube at any point of time? 
    # 50% its 3 and 50% - it is 2 or 1 faces(depending on the angle). So, why 
    # waste resources drawing those if you cannot see them anyway?
    glEnable(GL_CULL_FACE);
    # do not draw back faces
    glCullFace(GL_FRONT);
    # faces are defined clock-wise
    glFrontFace(GL_CCW);
    
    glPushMatrix()
    gluLookAt(eyex, eyey, eyez, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glColor3f(1.0, 1.0, 1.0)
    #Ground()
    
    if jump:
        glTranslatef(cx, cy, cz)
    Cube(image, data, texID)
    glPopMatrix()
    
    pygame.display.flip()
    pygame.time.wait(60)
    
def game_loop():           
    gameExit = False
    print("Inside game_loop")
   
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.5, 50.0)

    cx = 0
    cy = 0
    cz = 0.0
    eyex = 0.0
    eyey = 0.0
    eyez = 15.0
    reset_x = 0.0
    reset_y = 0.0
    reset_z = 15.0
    eyex_change = 0.0
    eyey_change = 0.0
    eyez_change = 0.0
    delta = 0.8
    jump = False
    
    #Load the image
    image = pygame.image.load('happy_birthday.jpg')
    #Create a data string for use by openGl
    data = pygame.image.tostring(image, 'RGBA')
    #Gives an unbound texture name
    texID = glGenTextures(1)
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                   eyey_change = -delta
               elif event.key == pygame.K_DOWN:
                   eyey_change = delta
               elif event.key == pygame.K_LEFT:
                   eyex_change = -delta
               elif event.key == pygame.K_RIGHT:
                   eyex_change = delta
               elif event.key == pygame.K_w:
                   eyez_change = -delta
               elif event.key == pygame.K_s:
                   eyez_change = delta
               elif event.key == pygame.K_r:
                   eyex_change = 0.0
                   eyey_change = 0.0
                   eyez_change = 0.0
                   eyex = reset_x
                   eyey = reset_y
                   eyez = reset_z
               elif event.key == pygame.K_j:
                   jump = True
            elif event.type == pygame.KEYUP:
               if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                   eyey_change = 0
               elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   eyex_change = 0
               elif event.key == pygame.K_w or event.key == pygame.K_s:
                   eyez_change = 0                
                 
        if not jump:         
            eyex += eyex_change
            eyey += eyey_change
            eyez += eyez_change
        else:
            while cy <= 10:
                cy += delta
                update_display(eyex, eyey, eyez, cx, cy, cz, jump)
            while cy > 1:
                cy -= delta
                update_display(eyex, eyey, eyez, cx, cy, cz, jump)
            jump = False
                
        update_display(eyex, eyey, eyez, cx, cy, cz, jump, image, data, texID)

game_loop()
pygame.quit()


