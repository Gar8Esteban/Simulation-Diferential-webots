from tkinter import messagebox as MessageBox


class test:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def xTest(self):
        try:
            x = float(self.x)
            if abs(x) > 0.2114*0.4:
                MessageBox.showwarning('X', 'La entrada se encuentra fuera del rango máximo \n x= [-0.0846, 0.0846]')
            else:
                return x
        except:
            MessageBox.showerror('X', 'Dato no numérico')
            return None

    def yTest(self):
        try:
            y = float(self.y)
            if abs(y) > 0.2114 * 0.4:
                MessageBox.showwarning('Y', 'La entrada se encuentra fuera del rango máximo \n y= [-0.0846, 0.0846]')
            else:
                return y
        except:
            MessageBox.showerror('Y', 'Dato no numérico')
            return None

    def zTest(self):
        try:
            z = float(self.z)
            if z < 0.0614*0.4 or z > 0.3714*0.4:
                MessageBox.showwarning('Z', 'La entrada se encuentra fuera del rango máximo \n x= [-0.0246, 0.1486]')
            else:
                return z
        except:
            MessageBox.showerror('Y', 'Dato no numérico')
            return None
