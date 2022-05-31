import math
from tkinter import messagebox as MessageBox


class Inversa:
    def __init__(self, x=0.0, y=0.0, z=0.0, l1=0.16*0.4, l2=0.11279*0.4, l3=0.09864*0.4):
        self.x = x
        self.y = y
        self.z = z
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.r = math.sqrt(math.pow(y, 2) + math.pow(x, 2))
        self.d = z - l1

    def theta1(self):
        try:
            x = self.x
            y = self.y
            Th1 = 90 + round(math.degrees(math.atan2(y, x)))
            return Th1
        except:
            MessageBox.showerror('Angulo Base', 'Error al calcular el angulo')
            return None

    def codoArriba(self):
        r = self.r
        d = self.d
        l2 = self.l2
        l3 = self.l3
        h = math.sqrt(math.pow(r, 2) + math.pow(d, 2))
        Cth3 = (math.pow(h, 2) - math.pow(l2, 2) - math.pow(l3, 2)) / (2 * l2 * l3)
        try:
            Sth3 = math.sqrt(1 - math.pow(Cth3, 2))
            Th3 = round(math.degrees(math.atan2(Sth3, Cth3)))
            alpha = math.degrees(math.atan2(d, r))
            beta = math.degrees(math.atan2(-1 * l3 * Sth3, l2 + l3 * Cth3)) + 90
            Th2 = round(beta - alpha)
        except:
            MessageBox.showerror('Solución Codo Arriba', 'No se encontró solución')
            return None, None

        if abs(Th2) <= 90 and abs(Th3) <= 90:
            return Th2, Th3
        else:
            return None, None

    def codoAbajo(self):
        r = self.r
        d = self.d
        l2 = self.l2
        l3 = self.l3
        h = math.sqrt(math.pow(r, 2) + math.pow(d, 2))
        Cth3 = (math.pow(h, 2) - math.pow(l2, 2) - math.pow(l3, 2)) / (2 * l2 * l3)
        try:
            Sth3 = math.sqrt(1 - math.pow(Cth3, 2))
            Th3 = round(math.degrees(math.atan2(-Sth3, Cth3)))
            alpha = math.degrees(math.atan2(d, r))
            beta = math.degrees(math.atan2(-l3 * Sth3, l2 + l3 * Cth3))
            Th2 = 90 - round(beta + alpha)
        except:
            MessageBox.showerror('Solución Codo Abajo', 'No se encontró solución')
            return None, None

        if abs(Th2) <= 90 and abs(Th3) <= 90:
            return Th2, Th3
        else:
            return None, None


