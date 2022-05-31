import math
import numpy as np


class matrizH:
    def __init__(self, theta=0, dz=0.0, ax=0.0, alpha=0.0, beta=0.0, h=0.0):
        self.theta = math.radians(theta) + math.radians(beta)
        self.dz = dz + h
        self.ax = ax
        self.alpha = alpha
        self.S = math.sin(self.theta)
        self.C = math.cos(self.theta)
        self.Sa = math.sin(self.alpha)
        self.Ca = math.cos(self.alpha)

    def customMatrix(self):
        a = self.ax
        d = self.dz
        s = self.S
        c = self.C
        sa = self.Sa
        ca = self.Ca
        '''Fila 1----------------------------------------------------------------------------------------------------'''
        A11 = round(c, 4)
        A12 = round(-s * ca, 4)
        A13 = round(s * sa, 4)
        A14 = round(a * c, 4)
        '''Fila 2----------------------------------------------------------------------------------------------------'''
        A21 = round(s, 4)
        A22 = round(c * ca, 4)
        A23 = round(-c * sa, 4)
        A24 = round(a * s, 4)
        '''Fila 3----------------------------------------------------------------------------------------------------'''
        A31 = 0
        A32 = round(sa, 4)
        A33 = round(ca, 4)
        A34 = d
        '''Fila 4----------------------------------------------------------------------------------------------------'''
        A41 = 0
        A42 = 0
        A43 = 0
        A44 = 1
        '''Ensamble de la matriz-------------------------------------------------------------------------------------'''
        A = np.array([[A11, A12, A13, A14],
                      [A21, A22, A23, A24],
                      [A31, A32, A33, A34],
                      [A41, A42, A43, A44]])
        return A

    def matrixDefault(self, link):
        if link == 0:
            d = 0.16 * 0.4
            a = 0
            alpha = math.radians(90)
        elif link == 1:
            d = 0
            a = 0.11279 * 0.4
            alpha = 0
        else:
            d = 0
            a = 0.09864 * 0.4
            alpha = 0

        s = self.S
        c = self.C
        sa = math.sin(alpha)
        ca = math.cos(alpha)
        '''Fila 1----------------------------------------------------------------------------------------------------'''
        A11 = round(c, 4)
        A12 = round(-s * ca, 4)
        A13 = round(s * sa, 4)
        A14 = round(a * c, 4)
        '''Fila 2----------------------------------------------------------------------------------------------------'''
        A21 = round(s, 4)
        A22 = round(c * ca, 4)
        A23 = round(-c * sa, 4)
        A24 = round(a * s, 4)
        '''Fila 3----------------------------------------------------------------------------------------------------'''
        A31 = 0
        A32 = round(sa, 4)
        A33 = round(ca, 4)
        A34 = d
        '''Fila 4----------------------------------------------------------------------------------------------------'''
        A41 = 0
        A42 = 0
        A43 = 0
        A44 = 1
        '''Ensamble de la matriz-------------------------------------------------------------------------------------'''
        A = np.array([[A11, A12, A13, A14],
                      [A21, A22, A23, A24],
                      [A31, A32, A33, A34],
                      [A41, A42, A43, A44]])
        return A

