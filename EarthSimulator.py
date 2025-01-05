# This program simulates a 3D Earth
import pygame
import math
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


def read_texture(filename):
    # Read an image file and convert it to OpenGL-readable text ID format
    img = Image.open(filename)
    img_data = np.array(list(img.getdata()), np.int8)
    text_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return text_id


def main():
    pygame.init()
    display = (400, 400)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Earth 3D")
    pygame.key.set_repeat(1, 10)  # Allows press and hold of buttons
    gluPerspective(40, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  # Set initial zoom
    lastpos_x = 0
    lastpos_y = 0
    texture = read_texture('Images/world.jpg')

    while True:
        for event in pygame.event.get():  # User activities
            # Exit cleanly if user quits window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Rotation with arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    glRotatef(1, 0, 1, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    glRotatef(1, 0, -1, 0)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    glRotatef(1, -1, 0, 0)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    glRotatef(1, 1, 0, 0)
            # Zoom in out using mouse wheel
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Wheel rolled up
                    glScaled(1.05, 1.05, 1.05)
                if event.button == 5:  # Wheel rolled down
                    glScaled(0.95, 0.95, 0.95)
            # Zoom in out using keys j and l
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  # Zoom in
                    glScaled(1.05, 1.05, 1.05)
                if event.key == pygame.K_l:  # Zoom out
                    glScaled(0.95, 0.95, 0.95)
            # Rotate with mouse click and drag
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                dx = x - lastpos_x
                dy = y - lastpos_y
                mouse_state = pygame.mouse.get_pressed()
                if mouse_state[0]:
                    model_view = (GLfloat * 16)()
                    glGetFloatv(GL_MODELVIEW_MATRIX, model_view)
                    # To combine x-axis and y-axis rotation
                    temp = (GLfloat * 3)()
                    temp[0] = model_view[0] * dy + model_view[1] * dx
                    temp[1] = model_view[4] * dy + model_view[5] * dx
                    temp[2] = model_view[8] * dy + model_view[9] * dx
                    norm_xy = math.sqrt(temp[0] * temp[0]
                                        + temp[1] * temp[1] + temp[2] * temp[2])
                    glRotatef(math.sqrt(dx * dx + dy * dy),
                              temp[0]/norm_xy, temp[1]/norm_xy, temp[2]/norm_xy)
                lastpos_x = x
                lastpos_y = y
            # Create Sphere and wraps texture
            glEnable(GL_DEPTH_TEST)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            quadratic_obj = gluNewQuadric()
            gluQuadricTexture(quadratic_obj, GL_TRUE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture)
            gluSphere(quadratic_obj, 1, 50, 50)
            gluDeleteQuadric(quadratic_obj)
            glDisable(GL_TEXTURE_2D)
            # Display pygame window
            pygame.display.flip()
            pygame.time.wait(10)


main()
