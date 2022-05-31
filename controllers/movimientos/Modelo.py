import numpy as np
import math


class Model:
    def __init__(self, dt, distCM=0.135, r=0.075):
        self.dt = dt
        self.distCM = distCM
        self.r = r
        self.deltaPosglobal = np.array([[0],
                                        [0],
                                        [0]])
        self.posGlobal = np.array([[0],
                                   [0],
                                   [0]])
        self.dt = dt
        self.K = np.array([[1, 1],
                           [0, 0],
                           [-1 / distCM, 1 / distCM]])
        self.r_2 = r 

    def estimacionPosicion(self, velIzq, velDer, theta):
        vectorVel = np.array([[velIzq],
                              [velDer]])
        rz = np.array([[math.cos(theta), -math.sin(theta), 0],
                       [math.sin(theta), math.cos(theta), 0],
                       [0, 0, 1]])
        
        velocidad = np.dot(np.dot(0.5 * rz * self.r_2, self.K), vectorVel)
        self.deltaPosglobal = self.dt*velocidad
        self.posGlobal = self.posGlobal + self.deltaPosglobal
        return np.round(self.posGlobal, 4)
