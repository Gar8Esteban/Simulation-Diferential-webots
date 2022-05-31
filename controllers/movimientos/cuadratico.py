import math
import numpy as np
from tkinter import messagebox as MessageBox


class Cuadratico:
    def __init__(self, Qi, Qf, tm=5.0):
        self.Qi = Qi
        self.Qf = Qf
        self.tm = tm
        self.arrayT = []
        self.P1 = []
        self.P2 = []
        self.P3 = []
        self.W1 = []
        self.W2 = []
        self.W3 = []
        self.Wp1 = []
        self.Wp2 = []
        self.Wp3 = []

    def perfilCuadratico(self, joint):
        K = np.array([[0, 0, 0, 1],
                      [0, 0, 1, 0],
                      [math.pow(self.tm, 3), math.pow(self.tm, 2), self.tm, 1],
                      [3*math.pow(self.tm, 2), 2*self.tm, 1, 0]])
        if np.linalg.det(K) == 0:
            MessageBox.showerror('Tiempo invalido')
            return None
        else:
            Q1 = np.array([[self.Qi[0]],
                           [0],
                           [self.Qf[0]],
                           [0]])
            Q2 = np.array([[self.Qi[1]],
                           [0],
                           [self.Qf[1]],
                           [0]])
            Q3 = np.array([[self.Qi[2]],
                           [0],
                           [self.Qf[2]],
                           [0]])
            A0 = np.dot(np.linalg.inv(K), Q1)
            A1 = np.dot(np.linalg.inv(K), Q2)
            A2 = np.dot(np.linalg.inv(K), Q3)
            self.arrayT = np.arange(0, self.tm+self.tm/100.0, self.tm/100.0)
            if joint == 1:
                for t in self.arrayT:
                    self.P1.append(A0[0] * math.pow(t, 3) + A0[1] * math.pow(t, 2) + A0[2] * t + A0[3])
                    self.W1.append(3 * A0[0] * math.pow(t, 2) + 2 * A0[1] * t + A0[2])
                    self.Wp1.append(6 * A0[0] * t + 2 * A0[1])

                return np.round(self.P1), np.round(self.W1), np.round(self.Wp1)
            elif joint == 2:
                for t in self.arrayT:
                    self.P2.append(A1[0] * math.pow(t, 3) + A1[1] * math.pow(t, 2) + A1[2] * t + A1[3])
                    self.W2.append(3 * A1[0] * math.pow(t, 2) + 2 * A1[1] * t + A1[2])
                    self.Wp2.append(6 * A1[0] * t + 2 * A1[1])

                return np.round(self.P2), np.round(self.W2), np.round(self.Wp2)
            elif joint == 3:
                for t in self.arrayT:
                    self.P3.append(A2[0] * math.pow(t, 3) + A2[1] * math.pow(t, 2) + A2[2] * t + A2[3])
                    self.W3.append(3 * A2[0] * math.pow(t, 2) + 2 * A2[1] * t + A2[2])
                    self.Wp3.append(6 * A2[0] * t + 2 * A2[1])

                return np.round(self.P3), np.round(self.W3), np.round(self.Wp3)
            else:
                return None, None, None


def main():
    Qi = np.array([15, 27, -45])
    Qf = np.array([-27, 40, 35])
    C = Cuadratico(Qi, Qf)
    Q, Qp, Qpp = C.perfilCuadratico(3)
    print(Q)


if __name__ == '__main__':
    main()

