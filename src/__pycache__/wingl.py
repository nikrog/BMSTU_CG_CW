from math import radians, cos, sin

from PyQt5 import QtGui, QtOpenGL
from PyQt5.QtGui import QMatrix4x4, QCursor, QColor
from PyQt5.QtCore import Qt, QPoint


import OpenGL.GL as gl
from OpenGL import GLU
from OpenGL.arrays import vbo

import glm
import glfw
import numpy as np
from random import random, shuffle, choice
from copy import deepcopy

from time import time

import particle
from shader import Shader

from object import Object
from camera import Camera

from particle import Particle, setParticleAngle, setParticleSpeed

# Изменяемые параметры
# Водопад
lineStartWF = [-15, 0, 0]
lineEndWF = [15, 0, 0]

# Скала
lineStartRock = [-15, 0, 5]
lineEndRock = [15, 0, 5]

particalSize = 3

global day
day = 1

def setParticleSize(value):
    global particalSize

    particalSize = value

    if (particalSize < 0):
        particalSize = 1


def getParticleSize():
    return particalSize


def setHeightWF(value):
    global lineStartWF, lineEndWF, lineStartRock, lineEndRock

    lineStartWF[1] = value
    lineEndWF[1] = value
    lineStartRock[1] = value
    lineEndRock[1] = value


class winGL(QtOpenGL.QGLWidget):
    frames = 0
    time_start = time()
    fps = 0

    newParticlesMean = 50.0
    newParticlesVariance = 5.0

    active = True

    maxAge = 70

    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.camMode = False
        # self.setMouseTracking(self.camMode)
        self.cursor = QCursor()

        self.color = (255, 255, 255, 1.0)
        self.angle = 0

        self.object = Object()
        self.camera = Camera()

        self.waterfallReady = False

        # Для частиц водопада и водяного потока
        self.particlesNum = 1000

        self.waterfallParticles = self.createParticles(lineStartWF, lineEndWF)
        self.solidParticles = self.createParticles(lineStartRock, lineEndRock)
        self.allParticles = self.getAllParticles()

        self.particlesPositions = self.getParticlesPositions()
        self.particlesColors = self.getParticlesColor()

        # Модель, выводимая на экран

        # Скала
        self.solidRock = np.array(
            (
                (-15, -0.01, 0),
                (-15, -0.01, 5),
                (15, -0.01, 5),
                (15, -0.01, 0),

                (-15, -15, 0),
                (-15, -15, 5),
                (15, -15, 5),
                (15, -15, 0)
            ),
            dtype='float32')

        self.indicesRock = np.array(
            (
                0, 1, 3, 1, 2, 3,
                4, 5, 7, 5, 6, 7,
                0, 3, 4, 3, 4, 7,
                1, 2, 5, 2, 5, 6,
                0, 1, 4, 1, 4, 5,
                2, 3, 6, 3, 6, 7
            ),
            dtype='int32')
        '''
        self.colorRock = [
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1)
        ]
        '''
        self.colorRock = [
            glm.vec4(0.439, 0.423, 0.423, 1),
            glm.vec4(0, 0.827, 0, 1),
            glm.vec4(0.439, 0.423, 0.423, 1),
            glm.vec4(0.439, 0.423, 0.423, 1)
        ]

        self.colorRock = np.array(self.colorRock, dtype="float32")

        self.solidRock2 = np.array(
            (
                (-20, 1, 0),
                (-20, 1, 5),
                (-15, 1, 5),
                (-15, 1, 0),

                (-20, -20, -2),
                (-20, -20, 5),
                (-15, -20, 5),
                (-15, -20, -2)
            ),
            dtype='float32')

        self.indicesRock2 = np.array(
            (
                0, 1, 3, 1, 2, 3,
                4, 5, 7, 5, 6, 7,
                0, 3, 4, 3, 4, 7,
                1, 2, 5, 2, 5, 6,
                0, 1, 4, 1, 4, 5,
                2, 3, 6, 3, 6, 7
            ),
            dtype='int32')
        self.solidRock2_copy = deepcopy(self.solidRock2)
        self.colorRock2 = [
            glm.vec4(0, 0.829, 0, 1),
            glm.vec4(0, 0.829, 0, 1),
            glm.vec4(0, 0.829, 0, 1),
            glm.vec4(0, 0.829, 0, 1)
        ]

        self.colorRock2 = np.array(self.colorRock2, dtype="float32")
        # Водное полотно
        self.solidWater = np.array(self.getGridCords(5, 15, [-15, -14.95, -20], 2, 5), dtype="float32")

        self.indicesWater = np.array(self.getGridIndices(5, 15), dtype="int32")

        self.colorWaterNP = np.array(self.getWaterColor(5, 15), dtype="float32")
        self.solidWater_copy = deepcopy(self.solidWater)

        # Озеро
        self.solidLake = np.array(
            (
                (-15, -15, 5),
                (-15, -15, -20),
                (15, -15, -20),
                (15, -15, 5),

                (-15, -20, 5),
                (-15, -20, -20),
                (15, -20, -20),
                (15, -20, 5)
            ),
            dtype='float32')

        self.indicesLake = np.array(
            (
                0, 1, 3, 1, 2, 3,
                4, 5, 7, 5, 6, 7,
                0, 3, 4, 3, 4, 7,
                1, 2, 5, 2, 5, 6,
                0, 1, 4, 1, 4, 5,
                2, 3, 6, 3, 6, 7
            ),
            dtype='int32')

        self.solidLake_copy = deepcopy(self.solidLake)

        self.colorLake = [
            glm.vec4(0, 0.584, 0.713, 1),
            glm.vec4(0, 0.584, 0.713, 1),
            glm.vec4(0, 0.584, 0.713, 1),
            glm.vec4(0, 0.584, 0.713, 1)
        ]
        self.colorLake = np.array(self.colorLake, dtype="float32")

        # Трава
        self.solidGrass = np.array(
            (
                (-20, -15, 5),
                (-20, -15, -20),
                (-15, -15, -20),
                (-15, -15, 5),

                (-20, -20, 5),
                (-20, -20, -20),
                (-10, -20, -20),
                (-15, -20, 5),
            ),
            dtype='float32')

        self.indicesGrass = np.array(
            (
                0, 1, 3, 1, 2, 3,
                4, 5, 7, 5, 6, 7,
                0, 3, 4, 3, 4, 7,
                1, 2, 5, 2, 5, 6,
                0, 1, 4, 1, 4, 5,
                2, 3, 6, 3, 6, 7,
            ),
            dtype='int32')
        self.solidGrass_copy = deepcopy(self.solidGrass)
        self.colorGrass = [
            glm.vec4(0, 0.827, 0, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0, 0.827, 0, 1)
        ]
        self.colorGrass = np.array(self.colorGrass, dtype="float32")

        # Трава
        self.solidGrass2 = np.array(
            (
                (20, -15, 5),
                (20, -15, -20),
                (15, -15, -20),
                (15, -15, 5),

                (20, -20, 5),
                (20, -20, -20),
                (10, -20, -20),
                (15, -20, 5)
            ),
            dtype='float32')

        self.indicesGrass2 = np.array(
            (
                0, 1, 3, 1, 2, 3,
                4, 5, 7, 5, 6, 7,
                0, 3, 4, 3, 4, 7,
                1, 2, 5, 2, 5, 6,
                0, 1, 4, 1, 4, 5,
                2, 3, 6, 3, 6, 7
            ),
            dtype='int32')
        self.solidGrass2_copy = deepcopy(self.solidGrass2)

        self.colorGrass2 = [
            glm.vec4(0, 0.827, 0, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0, 0.827, 0, 1)
        ]
        self.colorGrass2 = np.array(self.colorGrass2, dtype="float32")

    def getWaterColor(self, height, width):
        global day

        colors = []
        if day:
            #colorTypes = [glm.vec4(0, 0.584, 0.713, 1),
                        #glm.vec4(0.450, 0.713, 0.996, 1)]
            colorTypes = [glm.vec4(0, 0.584, 0.713, 1),
                        glm.vec4(0.5, 0.8, 1, 1)]
        else:
            colorTypes = [glm.vec4(0, 0.584, 0.713, 1),
                          glm.vec4(0.5, 0.7, 0.9, 1)]

        for i in range((height + 1) * (width + 1)):
            element = choice(colorTypes)
            colors.append(element)

        return colors

    def getGridIndices(self, height, width):

        allIndices = []

        for i in range(height):

            indices = []

            for j in range(width):
                indices.append((i * (width + 1)) + j)
                indices.append((i * (width + 1)) + (j + 1))
                indices.append(((i + 1) * (width + 1)) + (j + 1))

                indices.append((i * (width + 1)) + j)
                indices.append(((i + 1) * (width + 1)) + j)
                indices.append(((i + 1) * (width + 1)) + (j + 1))

            if (i % 2 == 1):
                indices.reverse()

            allIndices.extend(indices)

        return allIndices

    def getGridCords(self, height, width, cord, stepX, stepZ):

        cords = []

        x = cord[0]
        y = cord[1]
        z = cord[2]

        for i in range(0, height + 1):
            for j in range(0, width + 1):
                cords.append(np.array((x + j * stepX, y, z + i * stepZ), dtype="float32"))

        return cords

    def changecolor(self):
        global day
        self.qglClearColor(QtGui.QColor(69, 65, 92))
        day = 0
        self.colorWaterNP = np.array(self.getWaterColor(5, 15), dtype="float32")
        self.colorGrass = [
            glm.vec4(0, 0.700, 0, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0, 0.700, 0, 1)
        ]
        self.colorGrass = np.array(self.colorGrass, dtype="float32")
        self.colorGrass2 = self.colorGrass

    def changecolor2(self):
        global day
        self.qglClearColor(QtGui.QColor(192, 232, 235))
        day = 1
        self.colorWaterNP = np.array(self.getWaterColor(5, 15), dtype="float32")
        self.colorGrass = [
            glm.vec4(0, 0.827, 0, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0.396, 0.262, 0.129, 1),
            glm.vec4(0, 0.827, 0, 1)
        ]
        self.colorGrass = np.array(self.colorGrass, dtype="float32")
        self.colorGrass2 = self.colorGrass

    def initializeGL(self):
        print("START Init")
        self.qglClearColor(QtGui.QColor(192, 232, 235))
        gl.glEnable(gl.GL_DEPTH_TEST)
        lightpos = (1.0, 1.0, 1.0)
        ambient = (0.7, 0.7, 0.7, 1)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightpos)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, ambient)

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        self.camera.changePerspective(ratio=width / height)
        self.camera.setPos([-37, 15, -35])
        self.camera.spinY(130)
        self.camera.spinX(-35)
        '''
        self.camera.setPos([0, 30, -70])
        self.camera.spinY(180)
        self.camera.spinX(-35)
        '''

    def paintSolidObject(self, vrtxs, indices, color):
        objectVBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, objectVBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vrtxs, gl.GL_STATIC_DRAW)

        objectEBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, objectEBO)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices, gl.GL_STATIC_DRAW)

        objectColorVBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, objectColorVBO)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, color, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 0, None)
        gl.glEnableVertexAttribArray(0)

        gl.glEnableVertexAttribArray(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, objectColorVBO)
        gl.glVertexAttribPointer(1, 4, gl.GL_FLOAT, True, 0, None)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, objectEBO)

        gl.glDrawElements(gl.GL_TRIANGLES, 1000, gl.GL_UNSIGNED_INT, None)

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)

    def init_pos_WF(self):
        self.solidRock = np.array(
            (
                (-15, -0.01, 0),
                (-15, -0.01, 5),
                (15, -0.01, 5),
                (15, -0.01, 0),

                (-15, -15, 0),
                (-15, -15, 5),
                (15, -15, 5),
                (15, -15, 0)
            ),
            dtype='float32')
        self.solidRock2 = np.array(
            (
                (-20, 1, 0),
                (-20, 1, 5),
                (-15, 1, 5),
                (-15, 1, 0),

                (-20, -20, -2),
                (-20, -20, 5),
                (-15, -20, 5),
                (-15, -20, -2)
            ),
            dtype='float32')
        self.solidGrass = np.array(
            (
                (-20, -15, 5),
                (-20, -15, -20),
                (-15, -15, -20),
                (-15, -15, 5),

                (-20, -20, 5),
                (-20, -20, -20),
                (-10, -20, -20),
                (-15, -20, 5),
            ),
            dtype='float32')
        self.solidGrass2 = np.array(
            (
                (20, -15, 5),
                (20, -15, -20),
                (15, -15, -20),
                (15, -15, 5),

                (20, -20, 5),
                (20, -20, -20),
                (10, -20, -20),
                (15, -20, 5)
            ),
            dtype='float32')
        self.solidLake = np.array(
            (
                (-15, -15, 5),
                (-15, -15, -20),
                (15, -15, -20),
                (15, -15, 5),

                (-15, -20, 5),
                (-15, -20, -20),
                (15, -20, -20),
                (15, -20, 5)
            ),
            dtype='float32')
        self.solidWater = np.array(self.getGridCords(5, 15, [-15, -14.95, -20], 2, 5), dtype="float32")

    def rotate_scene_oz(self, teta):
        x_c = 0
        y_c = 0
        for i in range(len(self.solidRock)):
            x_c += self.solidRock[i][0]
            y_c += self.solidRock[i][1]
            x_c += self.solidLake[i][0]
            y_c += self.solidLake[i][1]
            x_c += self.solidGrass[i][0]
            y_c += self.solidGrass[i][1]
            x_c += self.solidGrass2[i][0]
            y_c += self.solidGrass2[i][1]
        x_c /= 32
        y_c /= 32
        for i in range(len(self.solidRock)):
            x_pr = self.solidRock[i][0]
            y_pr = self.solidRock[i][1]
            self.solidRock[i][0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
            self.solidRock[i][1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
            x_pr = self.solidLake[i][0]
            y_pr = self.solidLake[i][1]
            self.solidLake[i][0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
            self.solidLake[i][1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
            x_pr = self.solidGrass[i][0]
            y_pr = self.solidGrass[i][1]
            self.solidGrass[i][0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
            self.solidGrass[i][1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
            x_pr = self.solidGrass2[i][0]
            y_pr = self.solidGrass2[i][1]
            self.solidGrass2[i][0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
            self.solidGrass2[i][1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
        '''
        x_pr = lineStartWF[0]
        y_pr = lineStartWF[1]
        lineStartWF[0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
        lineStartWF[1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
        x_pr = lineEndWF[0]
        y_pr = lineEndWF[1]
        lineEndWF[0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
        lineEndWF[1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
        x_pr = lineStartRock[0]
        y_pr = lineStartRock[1]
        lineStartRock[0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
        lineStartRock[1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
        x_pr = lineEndRock[0]
        y_pr = lineEndRock[1]
        lineEndRock[0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
        lineEndRock[1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
        '''
        for i in range(len(self.solidWater)):
            x_pr = self.solidWater[i][0]
            y_pr = self.solidWater[i][1]
            self.solidWater[i][0] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
            self.solidWater[i][1] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)

        particles = self.getAllParticles()
        for i in range(len(particles)):
            pos = particles[i].get_pos()
            x_pr = pos[0]
            y_pr = pos[1]
            pos[1] = x_c + (x_pr - x_c) * cos(teta) - (y_pr - y_c) * sin(teta)
            pos[2] = y_c + (x_pr - x_c) * sin(teta) + (y_pr - y_c) * cos(teta)
            particles[i].set_pos(pos)
        for i in range(len(particles)):
            particles[i].age = particles[i].maxAge + 1
        self.deleteExtraParticles()

    def rotate_scene_oy(self, teta):
        x_c = 0
        z_c = 0
        for i in range(len(self.solidRock)):
            x_c += self.solidRock[i][0]
            z_c += self.solidRock[i][2]
            x_c += self.solidLake[i][0]
            z_c += self.solidLake[i][2]
            x_c += self.solidGrass[i][0]
            z_c += self.solidGrass[i][2]
            x_c += self.solidGrass2[i][0]
            z_c += self.solidGrass2[i][2]
        x_c /= 32
        z_c /= 32
        for i in range(len(self.solidRock)):
            x_pr = self.solidRock[i][0]
            z_pr = self.solidRock[i][2]
            self.solidRock[i][0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
            self.solidRock[i][2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            x_pr = self.solidLake[i][0]
            z_pr = self.solidLake[i][2]
            self.solidLake[i][0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
            self.solidLake[i][2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            x_pr = self.solidGrass[i][0]
            z_pr = self.solidGrass[i][2]
            self.solidGrass[i][0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
            self.solidGrass[i][2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            x_pr = self.solidGrass2[i][0]
            z_pr = self.solidGrass2[i][2]
            self.solidGrass2[i][0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
            self.solidGrass2[i][2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        '''
        x_pr = lineStartWF[0]
        z_pr = lineStartWF[2]
        lineStartWF[0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
        lineStartWF[2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        x_pr = lineEndWF[0]
        z_pr = lineEndWF[2]
        lineEndWF[0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
        lineEndWF[2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        x_pr = lineStartRock[0]
        z_pr = lineStartRock[2]
        lineStartRock[0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
        lineStartRock[2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        x_pr = lineEndRock[0]
        z_pr = lineEndRock[2]
        lineEndRock[0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
        lineEndRock[2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        '''

        for i in range(len(self.solidWater)):
            x_pr = self.solidWater[i][0]
            z_pr = self.solidWater[i][2]
            self.solidWater[i][0] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
            self.solidWater[i][2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)

        particles = self.getAllParticles()

        for i in range(len(particles)):
            pos = particles[i].get_pos()
            x_pr = pos[0]
            z_pr = pos[2]
            pos[1] = x_c + (x_pr - x_c) * cos(teta) + (z_pr - z_c) * sin(teta)
            pos[2] = z_c - (x_pr - x_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            particles[i].set_pos(pos)

        for i in range(len(particles)):
            particles[i].age = particles[i].maxAge + 1


    def rotate_scene_ox(self, teta):
        y_c = 0
        z_c = 0
        for i in range(len(self.solidRock)):
            y_c += self.solidRock[i][1]
            z_c += self.solidRock[i][2]
            y_c += self.solidLake[i][1]
            z_c += self.solidLake[i][2]
            y_c += self.solidGrass[i][1]
            z_c += self.solidGrass[i][2]
            y_c += self.solidGrass2[i][1]
            z_c += self.solidGrass2[i][2]
        y_c /= 32
        z_c /= 32
        for i in range(len(self.solidRock)):
            y_pr = self.solidRock[i][1]
            z_pr = self.solidRock[i][2]
            self.solidRock[i][1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
            self.solidRock[i][2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            y_pr = self.solidLake[i][1]
            z_pr = self.solidLake[i][2]
            self.solidLake[i][1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
            self.solidLake[i][2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            y_pr = self.solidGrass[i][1]
            z_pr = self.solidGrass[i][2]
            self.solidGrass[i][1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
            self.solidGrass[i][2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            y_pr = self.solidGrass2[i][1]
            z_pr = self.solidGrass2[i][2]
            self.solidGrass2[i][1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
            self.solidGrass2[i][2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        '''
        y_pr = lineStartWF[1]
        z_pr = lineStartWF[2]
        lineStartWF[1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
        lineStartWF[2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        y_pr = lineEndWF[1]
        z_pr = lineEndWF[2]
        lineEndWF[1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
        lineEndWF[2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        y_pr = lineStartRock[1]
        z_pr = lineStartRock[2]
        lineStartRock[1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
        lineStartRock[2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        y_pr = lineEndRock[1]
        z_pr = lineEndRock[2]
        lineEndRock[1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
        lineEndRock[2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
        '''

        for i in range(len(self.solidWater)):
            y_pr = self.solidWater[i][1]
            z_pr = self.solidWater[i][2]
            self.solidWater[i][1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
            self.solidWater[i][2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)


        particles = self.getAllParticles()
        for i in range(len(particles)):
            pos = particles[i].get_pos()
            y_pr = pos[1]
            z_pr = pos[2]
            pos[1] = y_c + (y_pr - y_c) * cos(teta) - (z_pr - z_c) * sin(teta)
            pos[2] = z_c + (y_pr - y_c) * sin(teta) + (z_pr - z_c) * cos(teta)
            particles[i].set_pos(pos)

        for i in range(len(particles)):
            particles[i].age = particles[i].maxAge + 1

    def paintDynamicObject(self, positions, colors):
        # Копирование массива вершин в вершинный буфер
        VBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, positions, gl.GL_STATIC_DRAW)

        colorVBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, colorVBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, colors, gl.GL_STATIC_DRAW)

        # Установка указателей вершинных атрибутов
        gl.glEnableVertexAttribArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 0, None)

        gl.glEnableVertexAttribArray(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, colorVBO)
        gl.glVertexAttribPointer(1, 4, gl.GL_FLOAT, True, 0, None)

        gl.glVertexAttribDivisor(0, 0)
        gl.glVertexAttribDivisor(1, 0)

        gl.glPointSize(particalSize)
        gl.glDrawArrays(gl.GL_POINTS, 0, len(self.allParticles))

    def paintGL(self):
        # # print("Paint START")

        # Очищаем экран
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Создание объекта вершинного массива
        VAO = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(VAO)

        # Установка шейдеров
        shaders = Shader("shader.vs", "shader.fs")
        shaders.use()

        # Преобразование
        shaders.setMat4("perspective", self.camera.getProjMatrix())
        shaders.setMat4("view", self.camera.getViewMatrix())
        shaders.setMat4("model", self.object.getModelMatrix())

        # Скала
        self.paintSolidObject(self.solidRock, self.indicesRock, self.colorRock)
        #self.paintSolidObject(self.solidRock2, self.indicesRock2, self.colorRock2)

        self.paintSolidObject(self.solidGrass, self.indicesGrass, self.colorGrass)
        self.paintSolidObject(self.solidGrass2, self.indicesGrass2, self.colorGrass2)

        # Озеро
        self.paintSolidObject(self.solidLake, self.indicesLake, self.colorLake)

        # Водное полотно
        self.paintSolidObject(self.solidWater, self.indicesWater, self.colorWaterNP)

        # Водопад
        self.paintDynamicObject(self.particlesPositions, self.particlesColors)

        # FPS счетчик

        self.frames = self.frames + 1
        time_end = time()

        if (time_end - self.time_start > 0):
            self.fps = self.frames // (time_end - self.time_start)
            self.frames = 0
            self.time_start = time_end

    def getFPS(self):
        return self.fps

    def getAmountParticles(self):
        return len(self.allParticles)

    def getAllParticles(self):
        allParticles = []
        if (self.waterfallReady):
            allParticles.extend(self.waterfallParticles)
        allParticles.extend(self.solidParticles)

        return allParticles

    def createParticles(self, lineStart, lineEnd):

        particles = []

        for i in range(self.particlesNum):
            particles.append(Particle(lineStart, lineEnd))

        return particles

    def getParticlesColor(self):
        colors = []

        check = True
        num = 0

        for particle in self.allParticles:
            colors.append(particle.getColor())

        npColors = np.array(colors)

        return npColors

    def getParticlesPositions(self):
        positions = []
        colors = []

        for particle in self.allParticles:
            positions.append(particle.getPosition())
            colors.append(particle.getColor())

        self.particlesColors = np.array(colors)
        poses = np.array(positions)

        return poses

    def moveParticles(self):

        if (self.waterfallReady):
            for particle in self.waterfallParticles:
                particle.moveWaterfallParticle()

        for particle in self.solidParticles:
            particle.moveSolidParticle()

        allParticles = []
        if (self.waterfallReady):
            allParticles.extend(self.waterfallParticles)
        allParticles.extend(self.solidParticles)

        return allParticles

    def changeParticles(self):
        self.allParticles = self.moveParticles()

        self.particlesPositions = self.getParticlesPositions()
        self.particlesColors = self.getParticlesColor()

    def makeWaterfall(self):

        self.deleteExtraParticles()

        # Добавить еще частиц
        extraParticlesNum = int(self.newParticlesMean + random() * self.newParticlesVariance)

        for i in range(extraParticlesNum):
            self.waterfallParticles.append(Particle(lineStartWF, lineEndWF))

        for i in range(int(extraParticlesNum * 1.5)):
            self.solidParticles.append(Particle(lineStartRock, lineEndRock))

        self.particlesNum += extraParticlesNum

        # Обновить атрибуты для всех частиц
        self.changeParticles()

    def deleteExtraParticles(self):
        deletedParticles = 0

        # Удалить упавшие капли
        for particle in self.waterfallParticles:
            if (particle.age > particle.maxAge):
                self.waterfallParticles.pop(0)
                deletedParticles += 1

        for particle in self.solidParticles:
            if (particle.pos[2] < 0):
                self.waterfallReady = True
                self.solidParticles.pop(0)
                deletedParticles += 1

        self.allParticles = self.getAllParticles()

        self.particlesNum -= deletedParticles

    def translate(self, vec):
        self.camera.translate(*vec)

    def scale(self, k):
        self.camera.zoom(k)

    def spin(self, vec):
        self.camera.spinX(vec[0])
        self.camera.spinY(vec[1])
        self.camera.spinZ(vec[2])

    # Изменение параметров
    def changeParticlesAmount(self, value):
        self.newParticlesMean = value
        print(self.newParticlesMean)

    def changeSpeedWF(self, operation):
        setParticleSpeed(operation)

    def changeAngleWF(self, operation):
        setParticleAngle(operation)

    def changeHeightAliveWF(self, value):
        for particle in self.allParticles:
            particle.pos[1] = value

    def changeHeightRock(self, value):

        for i in range(4):
            self.solidRock[i][1] = value

    # Мышка
    def mousePressEvent(self, event):
        camPosition = self.pos()

        self.lastPos = QPoint(camPosition.x() + self.width() // 2,
                              camPosition.y() + self.height() // 2)

        print(self.camera.getPos())

        self.cursor.setPos(self.lastPos)
        self.cursor.setShape(Qt.BlankCursor)

        if (event.button() == Qt.LeftButton):
            self.camMode = not self.camMode
            self.setMouseTracking(self.camMode)

        if (self.camMode):
            print("Dynamic CAM: On")
        else:
            print("Dynamic CAM: Off")

    def mouseMoveEvent(self, event):
        curPos = event.globalPos()

        if (self.lastPos == curPos):
            return

        deltaX = curPos.x() - self.lastPos.x()
        deltaY = self.lastPos.y() - curPos.y()
        self.lastPos = curPos

        self.camera.rotation(deltaX, deltaY)

    def wheelEvent(self, event):
        print("wheel")
        zoomK = event.pixelDelta().y() / 100
        self.camera.zoom(zoomK)

    def update(self, color, translateVec):
        self.camera.continousTranslate(translateVec)
        self.color = color
        self.updateGL()

    def updateWaterColor(self):
        np.random.shuffle(self.colorWaterNP)

