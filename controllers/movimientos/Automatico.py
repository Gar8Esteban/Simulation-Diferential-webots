import numpy as np
import math
import time
try:
    from controller import Motor
except:
    pass


class control:
    def __init__(self):
        self.eK1_angle = 0.0
        self.eK2_angle = 0.0
        self.uK1_angle = 0.0
        self.ek1_pos = 0.0
        self.ek2_pos = 0.0
        self.uK1_pos = 0.0
        self.wD = 0.0
        self.wI = 0.0

    def oriPID(self, t, ta, Ts=0.001, m1=0, m2=0):
        errorOri = math.atan2(math.sin(t-ta), math.cos(t-ta))
        Kp = 2.1 #Presente
        Ki = 1.2#pasado
        Kd = 0.01#fururo
        t0 = Kp + Kd/Ts + (Ki*Ts)/2
        t1 = -Kp - (2*Kd)/Ts + (Ki*Ts)/2
        t2 = Kd/Ts
        if abs(errorOri) > 0.01:
            #print(errorOri)
            uKangle = t0*errorOri + t1*self.eK1_angle + t2*self.eK2_angle + self.uK1_angle
            self.eK2_angle = self.eK1_angle
            self.eK1_angle = errorOri
            self.uK1_angle = uKangle
            self.wD = (2*self.uK1_angle*0.135)/(2*0.075)
            self.wI = (-2*self.uK1_angle*0.135)/(2*0.075)
            try:
                if self.wI > 10:
                    self.wI = 10
                if self.wD > 10:
                    self.wD = 10
                if self.wI < -10:
                    self.wI = 10
                if self.wD < -10:
                    self.wD = 10
                m1.setVelocity(round(self.wI, 4))
                m2.setVelocity(round(self.wD, 4))
            except:
                pass

            return 0
        else:
            return 1

    def posPID(self, x, y, xa, ya, Ts=0.001, m1=0, m2=0):
        errorPos = math.sqrt(math.pow(x-xa, 2) + math.pow(y-ya, 2))
        Kp = 1.5 #Presente
        Ki = 0.1#pasado
        Kd = 0#fururo
        t0 = Kp + Kd/Ts + (Ki*Ts)/2
        t1 = -Kp - (2*Kd)/Ts + (Ki*Ts)/2
        t2 = Kd/Ts
        disDes = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        disAct = math.sqrt(math.pow(xa, 2) + math.pow(ya, 2))
        if disAct > disDes:
            errorPos = -errorPos
        if abs(errorPos) > 0.025:
            uKangle = t0*errorPos + t1*self.ek1_pos + t2*self.ek2_pos + self.uK1_pos
            self.ek2_pos = self.ek1_pos
            self.ek1_pos = errorPos
            self.uK1_pos = uKangle
            velD = self.uK1_pos / 0.075
            velI = self.uK1_pos / 0.075
            try:
                if velI > 10:
                    velI = 10
                if velD > 10:
                    velD = 10
                if velI < -10:
                    velI = 10
                if velD < -10:
                    velD = 10
                m1.setVelocity(round(velI, 4))
                m2.setVelocity(round(velD, 4))
                print(errorPos)
            except:
                pass
            return 0
        else:
            m1.setVelocity(0)
            m2.setVelocity(0)
            return 1













