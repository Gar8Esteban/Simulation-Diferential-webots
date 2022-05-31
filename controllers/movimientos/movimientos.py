"""movimientos controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import PositionSensor
from controller import Motor
import threading
import Interfaz as inter
from controller import InertialUnit
from controller import GPS
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
mot1 = Motor("m1")
mot2 = Motor("m2")
motHombro = Motor('motorHombro')
motBrazo = Motor('motorBrazo')
motAnte = Motor('motorAnteBrazo')
motGarra = Motor('motorGarra')


mot1.setPosition(float('inf'))
mot2.setPosition(float('inf'))


mot1.setVelocity(0)
mot2.setVelocity(0)

imu = InertialUnit('IMU')
imu.enable(1)

gps = GPS('gps')
gps.enable(1)

sensorBase = PositionSensor('Posicion_Base')
sensorBrazo = PositionSensor('Pos_Brazo')
sensorAntebrazo = PositionSensor('Pos_Antebrazo')

sensorBase.enable(1)
sensorBrazo.enable(1)
sensorAntebrazo.enable(1)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
def principal():
    while robot.step(timestep) != -1:
        # Read the sensors:
        # Enter here functions to read sensor data, like:
        #  val = ds.getValue()
        # Process sensor data here.
    
    
        # Enter here functions to send actuator commands, like:
        #  motor.setPosition(10.0)
        pass
    

guideThread = threading.Thread(target=principal, daemon=True)
guideThread.start()


if __name__ == '__main__':
    gd = inter.GUI(mot1, mot2, imu, gps, motHombro,motBrazo,
                   motAnte, motGarra, sensorBase, sensorBrazo, sensorAntebrazo)
    gd.guide()

# Enter here exit cleanup code.
