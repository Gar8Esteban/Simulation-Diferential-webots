try:
    from controller import Robot
    from controller import PositionSensor
    from controller import Motor
    from controller import Connector
except:
    print('webots')
    pass

import math


class mover:
    def __init__(self, mBase, mBrazo, mAntebrazo, gripper):
        self.mBase = mBase
        self.mBrazo = mBrazo
        self.mAntebrazo = mAntebrazo
        self.gripper = gripper

    def moverScaleboton(self, link, position):
        if link == 0:
            try:
                self.mBase.setPosition(math.radians(position))
            except:
                pass
        elif link == 1:
            try:
                self.mBrazo.setPosition(math.radians(position))
            except:
                pass
        elif link == 2:
            try:
                self.mAntebrazo.setPosition(math.radians(position))
            except:
                pass

    def setHome(self):
        try:
            self.mBase.setPosition(0.0)
            self.mBrazo.setPosition(0.0)
            self.mAntebrazo.setPosition(0.0)
        except:
            pass

    def moverForzado(self, link, position):
        if link == 0:
            self.mBase.setPosition(math.radians(position))
        elif link == 1:
            self.mBrazo.setPosition(math.radians(position))
        elif link == 2:
            self.mAntebrazo.setPosition(math.radians(position))

