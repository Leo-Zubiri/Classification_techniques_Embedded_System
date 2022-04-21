import sys
# Modulo/clase arduino
import arduino as ard 
import time
from PyQt5 import uic, QtWidgets, QtCore
from pynput.keyboard import Key, Controller

qtCreatorFile = "MainWindow.ui" # Nombre del archivo .ui aqui.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals y Configuraciones Iniciales
        self.btn_conectar.clicked.connect(self.conectar)
        self.btn_agregar.clicked.connect(self.agregar)
        #self.btn_accion.clicked.connect(self.accion)
	 
        #Instanciamos un objeto de la clase marduino
        self.arduino = ard.c_arduino()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execTimer)
        self.teclado = Controller()
        

   
    def conectar(self):
        com = "COM"+self.txt_com.text()
        #print(com)
        # Inicializamos el arduino
        # Conexion a un puerto en LINUX /dev/tty
        # Enviar el COM que se ocupa en el dispositivo
        self.arduino.connect(com,self.btn_conectar)
        self.txt_com.setText("")
        if(self.arduino.verifyConnection()):
            # Si esta conectado...            
            self.txt_arduino.setEnabled(True)
            self.txt_arduino.setFocus()            
            self.beginRead()

    def beginRead(self):
        if self.arduino == None:
            # Inicializar Conexion con Arduino
            self.conectar()
            print("Arduino Conectado")

        if not self.timer.isActive():
            self.timer.start(10)
        else:
            self.timer.stop()

    # Timer para el Python
    def execTimer(self):
        if self.arduino.inWaiting():
            lectura = self.arduino.read()
            lectura = lectura.replace("\n", "")
            lectura = lectura.replace("\r", "")
            self.keystrokes(lectura)
            #print(lectura)


    def keystrokes(self,data = "00000"):
        if data == "00001":
            self.teclado.press('A')
            self.teclado.release('A')
        elif data == "00010":
            self.teclado.press('B')
            self.teclado.release('B')
        elif data == "00100":
            self.teclado.press('C')
            self.teclado.release('C')
        elif data == "01000":
            self.teclado.press('D')
            self.teclado.release('D')
        elif data == "10000":
            self.teclado.press('E')
            self.teclado.release('E')
        
    
    def agregar(self):
        dato = self.txt_arduino.text()
        self.list_datos.addItem(dato)        
        self.txt_arduino.setText("")
        self.txt_arduino.setFocus() 


    def closeEvent(self, event):
        self.arduino.disconnect()
        if self.timer.isActive():
            self.timer.stop()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
