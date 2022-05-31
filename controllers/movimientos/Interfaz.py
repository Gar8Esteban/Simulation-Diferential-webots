import tkinter
from tkinter import ttk
from tkinter import *
import numpy as np
import Wheels as wh
import math
import time
import threading
import Automatico as auto
import moverAntropomorfico as movAntro
import matrizHomogenea as mH
import inversaAntropomorfico as invAntro
import testDatainverse as testD
from tkinter import messagebox as MessageBox
import cuadratico

try:
    from controller import Robot
    from controller import PositionSensor
    from controller import Motor
    from controller import Connector
    from controller import InertialUnit
except:
    pass


class GUI:
    def __init__(self, m1, m2, imu, gps, mHombro, mBrazo, mAnte, mGarra, sensorBase, sensorBrazo, sensorAntebrazo):
        self.m1 = m1
        self.m2 = m2
        self.wh = wh.movimiento(m1, m2, imu=imu, gps=gps)
        self.mov = movAntro.mover(mHombro, mBrazo, mAnte, mGarra)
        self.anguloDes = math.radians(90)
        self.xDes = 0
        self.yDes = 0
        self.banderaAuto = 0
        self.anguloOri = 0
        self.sensorBase = sensorBase
        self.sensorBrazo = sensorBrazo
        self.sensorAntebrazo = sensorAntebrazo
        self.mBase = mHombro
        self.mBrazo = mBrazo
        self.mAntebrazo = mAnte

    def guide(self):
        def movDiferencial(d):
            self.banderaAuto = 0
            self.wh.direct(d)

        def velMotores(n):
            vel = sliderMotor.get()/10.0
            self.wh.setSpeed(vel)

        def automatico():
            xa, ya = self.wh.posCartesiano()
            x = float(entryXDeseado.get())
            y = float(entryYDeseado.get())
            oriXY = math.atan2(y-ya, x-xa)
            self.anguloOri = oriXY
            self.xDes = x
            self.yDes = y
            self.anguloDes = math.radians(float(entryAngleDeseado.get()))
            self.banderaAuto = 1

        def estPosicion():
            movAuto = auto.control()
            while True:
                t = -self.wh.angle()
                ''' + math.radians(180)'''
                x, y = self.wh.posCartesiano()
                textPosicionx.delete('1.0', 'end')
                textPosicionx.insert(END, str(x), 4)
                textPosiciony.delete('1.0', 'end')
                textPosiciony.insert(END, str(y), 4)
                textPosiciont.delete('1.0', 'end')
                textPosiciont.insert(END, str(math.degrees(round(t, 2))))
                if self.banderaAuto:
                    flagAng1 = movAuto.oriPID(t, self.anguloOri, m1=self.m1, m2=self.m2)
                    if flagAng1:
                        flagPos1 = movAuto.posPID(self.xDes, self.yDes, x, y, m1=self.m1, m2=self.m2)
                        if flagPos1:
                            print(1)
                time.sleep(0.001)

        def matrizFinal():
            matriz0 = mH.matrizH(theta=scaleHombro.get(), beta=90)
            matriz1 = mH.matrizH(theta=scaleBrazo.get(), beta=90)
            matriz2 = mH.matrizH(theta=scaleAntebrazo.get())

            A0 = matriz0.matrixDefault(0)
            A1 = matriz1.matrixDefault(1)
            A2 = matriz2.matrixDefault(2)
            Ag = np.dot(A0, A1)
            A = np.dot(Ag, A2)
            textEfector.delete('1.0', 'end')
            textEfector.insert(END, np.round(A, 4))

        def moverBase(int):
            self.mov.moverScaleboton(0, scaleHombro.get())
            matriz =  mH.matrizH(theta=scaleHombro.get(), beta=90)
            A = matriz.matrixDefault(0)
            textLink1.delete('1.0', 'end')
            textLink1.insert(END, A)
            matrizFinal()

        def moverBrazo(int):
            self.mov.moverScaleboton(1, scaleBrazo.get())
            matriz = mH.matrizH(theta=scaleHombro.get(), beta=90)
            A = matriz.matrixDefault(0)
            textLink1.delete('1.0', 'end')
            textLink1.insert(END, A)
            matrizFinal()

        def moverAntebrazo(int):
            self.mov.moverScaleboton(2, scaleAntebrazo.get())
            matriz = mH.matrizH(theta=scaleAntebrazo.get())
            A = matriz.matrixDefault(2)
            textLink3.delete('1.0', 'end')
            textLink3.insert(END, A)
            matrizFinal()

        def inverse(sol):
            test = testD.test(entryX.get(), entryY.get(), entryZ.get())
            x = test.xTest()
            y = test.yTest()
            z = test.zTest()
            inv = invAntro.Inversa(x, y, z)
            theta1 = inv.theta1()
            if sol:
                theta2, theta3 = inv.codoArriba()
            else:
                theta2, theta3 = inv.codoAbajo()
            if isinstance(theta1, int) and isinstance(theta2, int) and isinstance(theta3, int):
                textT1.delete('1.0', 'end')
                textT2.delete('1.0', 'end')
                textT3.delete('1.0', 'end')
                textT1.insert(END, theta1)
                textT2.insert(END, theta2)
                textT3.insert(END, theta3)
                matriz0 = mH.matrizH(theta=theta1, beta=90)
                matriz1 = mH.matrizH(theta=theta2, beta=90)
                matriz2 = mH.matrizH(theta=theta3)
                A0 = matriz0.matrixDefault(0)
                A1 = matriz1.matrixDefault(1)
                A2 = matriz2.matrixDefault(2)
                textLink1.delete('1.0', 'end')
                textLink1.insert(END, A0)
                textLink2.delete('1.0', 'end')
                textLink2.insert(END, A1)
                textLink3.delete('1.0', 'end')
                textLink3.insert(END, A2)
                A01 = np.dot(A0, A1)
                A = np.dot(A01, A2)
                textEfector.delete('1.0', 'end')
                textEfector.insert(END, np.round(A, 4))
                self.mov.moverScaleboton(0, theta1)
                self.mov.moverScaleboton(1, theta2)
                self.mov.moverScaleboton(2, theta3)
            else:
                textT1.delete('1.0', 'end')
                textT2.delete('1.0', 'end')
                textT3.delete('1.0', 'end')
                textLink1.delete('1.0', 'end')
                textLink2.delete('1.0', 'end')
                textLink3.delete('1.0', 'end')
                textEfector.delete('1.0', 'end')
                MessageBox.showwarning('Solucion no encontrada', 'revise datos de entrada o pruebe otra solución')

        def Cuadratica(sol, auto=False, xa=0.0, ya=0.0, za=0.0):
            if auto:
                x = xa
                y = ya
                z = za
            else:
                test = testD.test(entryXcuad.get(), entryYcuad.get(), entryZcuad.get())
                x = test.xTest()
                y = test.yTest()
                z = test.zTest()
            inv = invAntro.Inversa(x, y, z)
            theta1 = inv.theta1()
            if sol:
                theta2, theta3 = inv.codoArriba()
            else:
                theta2, theta3 = inv.codoAbajo()
            Qf = np.array([theta1, theta2, theta3])
            try:
                posBase = round(math.degrees(self.sensorBase.getValue()))
                posBrazo = round(math.degrees(self.sensorBrazo.getValue()))
                posAntebrazo = round(math.degrees(self.sensorAntebrazo.getValue()))
                Qi = np.array([posBase, posBrazo, posAntebrazo])
            except:
                Qi = np.array([30, 20, 10])
            solCuad = cuadratico.Cuadratico(Qi, Qf)
            posQ1, _, _ = solCuad.perfilCuadratico(1)
            posQ2, _, _ = solCuad.perfilCuadratico(2)
            posQ3, _, _ = solCuad.perfilCuadratico(3)
            tm = len(solCuad.arrayT)
            for n in range(tm):
                try:
                    self.mBase.setPosition(math.radians(float(posQ1[n])))
                    self.mBrazo.setPosition(math.radians(float(posQ2[n])))
                    self.mAntebrazo.setPosition(math.radians(float(posQ3[n])))
                    time.sleep(0.003)
                except:
                    pass

        def recogerPiezas():
            Cuadratica(1, True, 0.0732, 0.0, 0.0668)
            Cuadratica(1, True, 0.0314, 0.0, 0.1418)
            Cuadratica(1, True, -0.0314, 0.0, 0.1418)
            Cuadratica(1, True, -0.0714, 0.0, 0.0959)

        root = tkinter.Tk()
        root.title('Planta Inteligencia Artificial')
        root.geometry('400x500')
        '''panel 1 --------------------------------------------------------------------------------------------------'''
        panel1 = Frame(root, bg='gray26', width=390, height=280)
        panel1.place(x=5, y=5)

        Kin = ttk.Notebook(panel1)
        Kin.place(x=0, y=0)

        Direct = Frame(Kin, bg='gray26', width=385, height=275)
        botonAdelante = Button(Direct, fg='light gray', bg='DarkOrange1', text='Up', font=('Ubuntu Condensed', 11),
                               command=lambda: movDiferencial('w'))
        botonAdelante.place(x=50, y=20)

        '''Boton atras ---------------------------------------------------------------------------------------------'''
        botonAtras = Button(Direct, text='down', fg='light gray', bg='DarkOrange1', font=('Ubuntu Condensed', 11),
                            command=lambda: movDiferencial('s'))
        botonAtras.place(x=50, y=90)

        '''Boton CW -------------------------------------------------------------------------------------------'''
        botonCW = Button(Direct, text='CW', fg='light gray', bg='DarkOrange1', font=('Ubuntu Condensed', 11),
                         command=lambda: movDiferencial('a'))
        botonCW.place(x=90, y=55)

        '''Boton CCW -------------------------------------------------------------------------------------------'''
        botonCCW = Button(Direct, text='CCW', fg='light gray', bg='DarkOrange1', font=('Ubuntu Condensed', 11),
                          command=lambda: movDiferencial('d'))
        botonCCW.place(x=10, y=55)

        '''Boton Stop -------------------------------------------------------------------------------------------'''
        botonStop = Button(Direct, text='Stop', fg='light gray', bg='red', font=('Ubuntu Condensed', 11),
                           command=lambda: movDiferencial('x'))
        botonStop.place(x=10, y=125)

        '''Text box velocidad ---------------------------------------------------------------------------------------'''
        labelVelocidad = Label(Direct, text='Velocidad deseada[rad/s]:', fg='light gray', bg='gray26',
                               font=('Ubuntu Condensed', 11))
        labelVelocidad.place(x=10, y=175)
        labelVelx = Label(Direct, text='vel: ', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelVelx.place(x=10, y=200)
        sliderMotor = Scale(Direct, from_=0, to=20, orient=HORIZONTAL, length=200, showvalue=0, fg='light gray',
                            bg='DarkOrange1', font=('Ubuntu Condensed', 11), command=velMotores)
        sliderMotor.place(x=50, y=200)

        '''Brazo antropomorfico--------------------------------------------------------------------------------------'''
        antro = Frame(Kin, bg='gray26', width=385, height=275)
        labelHombro = Label(antro, text='Rotación del Hombro', fg='light gray', bg='gray26',
                            font=('Ubuntu Condensed', 11))
        labelHombro.place(x=5, y=40)
        scaleHombro = Scale(antro, from_=-180, to=180, orient=HORIZONTAL, length=200, showvalue=1, fg='light gray',
                            bg='DarkOrange1', font=('Ubuntu Condensed', 11), command=moverBase)
        scaleHombro.place(x=175, y=40)

        labelBrazo = Label(antro, text='Rotación del brazo', fg='light gray', bg='gray26',
                           font=('Ubuntu Condensed', 11))
        labelBrazo.place(x=5, y=100)
        scaleBrazo = Scale(antro, from_=-90, to=90, orient=HORIZONTAL, length=200, showvalue=1, fg='light gray',
                           bg='DarkOrange1', font=('Ubuntu Condensed', 11), command=moverBrazo)
        scaleBrazo.place(x=175, y=100)

        labelAntebrazo = Label(antro, text='Rotación del antebrazo', fg='light gray', bg='gray26',
                               font=('Ubuntu Condensed', 11))
        labelAntebrazo.place(x=5, y=160)
        scaleAntebrazo = Scale(antro, from_=-90, to=90, orient=HORIZONTAL, length=200, showvalue=1, fg='light gray',
                               bg='DarkOrange1', font=('Ubuntu Condensed', 11), command=moverAntebrazo)
        scaleAntebrazo.place(x=175, y=160)

        '''Solucion inversa------------------------------------------------------------------------------------------'''
        Inverse = Frame(Kin, bg='gray26', width=385, height=275)
        labelCoord = Label(Inverse, text='Coordenadas:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelCoord.place(x=10, y=10)
        'Cordenada x:'
        labelX = Label(Inverse, text='X:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelX.place(x=20, y=38)
        entryX = Entry(Inverse, bd=2, width=7)
        entryX.place(x=50, y=40)
        'Coordenada y:'
        labelY = Label(Inverse, text='Y:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelY.place(x=20, y=68)
        entryY = Entry(Inverse, bd=2, width=7)
        entryY.place(x=50, y=70)
        'Coordenada z:'
        labelZ = Label(Inverse, text='Z:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelZ.place(x=20, y=98)
        entryZ = Entry(Inverse, bd=2, width=7)
        entryZ.place(x=50, y=100)
        'Botones de la solución'
        labelType = Label(Inverse, text='Solución:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelType.place(x=10, y=130)
        buttonElbowUp = Button(Inverse, text='Codo Arriba', fg='light gray', bg='DarkOrange1',
                               font=('Ubuntu Condensed', 11), command=lambda: inverse(1))
        buttonElbowUp.place(x=10, y=170)
        buttonElbowDown = Button(Inverse, text='Codo Abajo', fg='light gray', bg='DarkOrange1',
                                 font=('Ubuntu Condensed', 11), command=lambda: inverse(0))
        buttonElbowDown.place(x=10, y=220)

        'etiquetas solución'
        labelTheta1 = Label(Inverse, text='Theta1:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelTheta1.place(x=150, y=38)
        textT1 = Text(Inverse, height=1, width=5)
        textT1.place(x=205, y=40)

        labelTheta2 = Label(Inverse, text='Theta2:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelTheta2.place(x=150, y=68)
        textT2 = Text(Inverse, height=1, width=5)
        textT2.place(x=205, y=70)

        labelTheta3 = Label(Inverse, text='Theta3:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelTheta3.place(x=150, y=98)
        textT3 = Text(Inverse, height=1, width=5)
        textT3.place(x=205, y=100)

        '''Perfil Cuadrático-----------------------------------------------------------------------------------------'''

        Cuadrado = Frame(Kin, bg='gray26', width=385, height=275)
        labelPosactual = Label(Cuadrado, text='Posición Efector (x, y, z) [m]:', fg='light gray', bg='gray26',
                               font=('Ubuntu Condensed', 11))
        labelPosactual.place(x=10, y=10)

        textEfectorpos = Text(Cuadrado, height=1, width=10)
        textEfectorpos.place(x=220, y=10)

        labelPosdeseada = Label(Cuadrado, text='Posición Deseada [m]:', fg='light gray', bg='gray26',
                                font=('Ubuntu Condensed', 11))
        labelPosdeseada.place(x=10, y=40)

        labelXcuad = Label(Cuadrado, text='X:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelXcuad.place(x=10, y=60)
        entryXcuad = Entry(Cuadrado, bd=2, width=7)
        entryXcuad.place(x=40, y=60)

        labelYcuad = Label(Cuadrado, text='Y:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelYcuad.place(x=10, y=80)
        entryYcuad = Entry(Cuadrado, bd=2, width=7)
        entryYcuad.place(x=40, y=80)

        labelZcuad = Label(Cuadrado, text='Z:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelZcuad.place(x=10, y=100)
        entryZcuad = Entry(Cuadrado, bd=2, width=7)
        entryZcuad.place(x=40, y=100)

        labelSolucioncuad = Label(Cuadrado, text='Método:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelSolucioncuad.place(x=10, y=140)

        buttonSolarriba = Button(Cuadrado, text='Codo Arriba', fg='light gray', bg='DarkOrange1',
                                 font=('Ubuntu Condensed', 11), command=lambda: Cuadratica(1))
        buttonSolarriba.place(x=10, y=180)

        buttonSolabajo = Button(Cuadrado, text='Codo Abajo', fg='light gray', bg='DarkOrange1',
                                font=('Ubuntu Condensed', 11), command=lambda: Cuadratica(0))
        buttonSolabajo.place(x=10, y=210)

        buttonPieza= Button(Cuadrado, text='Recoger', fg='light gray', bg='DarkOrange1',
                                font=('Ubuntu Condensed', 11), command=recogerPiezas)
        buttonPieza.place(x=100, y=210)

        '''Pestañas panel 1 -----------------------------------------------------------------------------------------'''
        Kin.add(Direct, text='Directa')
        Kin.add(antro, text='Antro')
        Kin.add(Inverse, text='Inversa')
        Kin.add(Cuadrado, text='Cuadrática')

        '''panel 2 -----------------------------------------------------------------------------------------------'''
        Panel2 = Frame(root, bg='gray26', width=390, height=200)
        Panel2.place(x=5, y=290)

        ventanasInfo = ttk.Notebook(Panel2)
        ventanasInfo.place(x=5, y=5)

        panelInfo = Frame(ventanasInfo, bg='gray26', width=375, height=200)


        '''Información global ---------------------------------------------------------------------------------------'''
        labelPosicionx = Label(panelInfo, text='x:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelPosicionx.place(x=10, y=30)
        textPosicionx = Text(panelInfo, height=1, width=5)
        textPosicionx.place(x=40, y=30)
        labelUnidadx = Label(panelInfo, text='[m]', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelUnidadx.place(x=90, y=30)

        labelPosiciony = Label(panelInfo, text='y:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelPosiciony.place(x=10, y=60)
        textPosiciony = Text(panelInfo, height=1, width=5)
        textPosiciony.place(x=40, y=60)
        labelUnidady = Label(panelInfo, text='[m]', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelUnidady.place(x=90, y=60)

        labelPosiciont = Label(panelInfo, text='T:', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelPosiciont.place(x=10, y=90)
        textPosiciont = Text(panelInfo, height=1, width=5)
        textPosiciont.place(x=40, y=90)
        labelUnidadt = Label(panelInfo, text='[deg]', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelUnidadt.place(x=90, y=90)

        labelAngleDeseado = Label(panelInfo, text='Angulo', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelAngleDeseado.place(x=180, y=30)
        entryAngleDeseado = Entry(panelInfo, width=10)
        entryAngleDeseado.place(x=240, y=30)

        labelXDeseado = Label(panelInfo, text='x', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelXDeseado.place(x=180, y=60)
        entryXDeseado = Entry(panelInfo, width=10)
        entryXDeseado.place(x=240, y=60)

        labelYDeseado = Label(panelInfo, text='y', fg='light gray', bg='gray26', font=('Ubuntu Condensed', 11))
        labelYDeseado.place(x=180, y=90)
        entryYDeseado = Entry(panelInfo, width=10)
        entryYDeseado.place(x=240, y=90)

        irBoton = Button(panelInfo, text='Ir', fg='light gray', bg='green', font=('Ubuntu Condensed', 11),
                         command=automatico)
        irBoton.place(x=180, y=130)
        '''Posiciones brazo antropomorfico---------------------------------------------------------------------------'''

        posAntro = Frame(Panel2, bg='gray26', width=385, height=275)
        Links = ttk.Notebook(posAntro)
        Links.place(x=5, y=5)

        '''link 1----------------------------------------------------------------------------------------------------'''
        link1 = Frame(Links, bg='white', width=375, height=200)
        textLink1 = Text(link1, height=5, width=40)
        textLink1.place(x=15, y=10)
        '''link 2----------------------------------------------------------------------------------------------------'''
        link2 = Frame(Links, bg='white', width=375, height=265)
        textLink2 = Text(link2, height=5, width=40)
        textLink2.place(x=15, y=10)
        '''link 3----------------------------------------------------------------------------------------------------'''
        link3 = Frame(Links, bg='white', width=375, height=265)
        textLink3 = Text(link3, height=5, width=40)
        textLink3.place(x=15, y=10)
        '''link e----------------------------------------------------------------------------------------------------'''
        linkE = Frame(Links, bg='white', width=375, height=265)
        textEfector = Text(linkE, height=5, width=40)
        textEfector.place(x=15, y=10)
        '''fin panel2------------------------------------------------------------------------------------------------'''
        Links.add(link1, text='Eslabón 1')
        Links.add(link2, text='Eslabón 2')
        Links.add(link3, text='Eslabón 3')
        Links.add(linkE, text='Posición Efector')

        ventanasInfo.add(panelInfo, text='información carro')
        ventanasInfo.add(posAntro, text='Posición')

        '''Posicion -------------------------------------------------------------------------------------------------'''
        hiloPosicion = threading.Thread(target=estPosicion, daemon=True)
        hiloPosicion.start()
        root.mainloop()


def main():
    G = GUI(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    G.guide()


if __name__ == '__main__':
    main()
