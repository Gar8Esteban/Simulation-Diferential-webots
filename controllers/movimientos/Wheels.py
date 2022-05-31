import numpy as np
import math
try:
    from controller import Robot
    from controller import PositionSensor
    from controller import Motor
    from controller import Connector
    from controller import InertialUnit
    from controller import GPS
except:
    pass


class movimiento:
    def __init__(self, m1, m2, vel=1.0, imu=0, gps=0):
        self.m1 = m1
        self.m2 = m2
        self.vel = float(vel)
        self.dir = [0, 0]
        self.imu = imu
        self.gps = gps

    def setSpeed(self, v):
        try:
            self.vel = float(v)
        except:
            pass

    def direct(self, d):
        if d == 'w':
            try:
                self.m1.setVelocity(self.vel)
                self.m2.setVelocity(self.vel)
                self.dir = [1, 1]
            except:
                pass
        elif d == 's':
            try:
                self.m1.setVelocity(-self.vel)
                self.m2.setVelocity(-self.vel)
                self.dir = [-1, -1]
            except:
                pass
        elif d == 'a':
            try:
                self.m1.setVelocity(self.vel)
                self.m2.setVelocity(-self.vel)
                self.dir = [1, -1]
            except:
                pass
        elif d == 'd':
            try:
                self.m1.setVelocity(-self.vel)
                self.m2.setVelocity(self.vel)
                self.dir = [-1, 1]
            except:
                pass
        elif d == 'x':
            try:
                self.m1.setVelocity(0)
                self.m2.setVelocity(0)
                self.dir = [0, 0]
            except:
                pass

    def angle(self):
        try:
            _, _, Yaw = self.imu.getRollPitchYaw()
            return Yaw
        except:
            return 0.0

    def posCartesiano(self):
        try:
            x, _, y = self.gps.getValues()
            return round(x, 4), round(y, 4)
        except:
            return 0.0, 0.0


def main(d):
    W = movimiento(0, 0)
    W.direct(d)


if __name__ == '__main__':
    main('z')
