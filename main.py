import sys
# Modulo/clase arduino
from PyQt5 import uic, QtWidgets, QtCore
from techniques.KNN import KNN

import arduinoWind as ard


qtCreatorFile = "main.ui" # Nombre del archivo .ui aqui.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals y Configuraciones Iniciales
        self.btnArduino.clicked.connect(self.conectar)
        self.btnIdentificar.clicked.connect(self.identificar)
        
        self.instancias = {
            "Cancer":"training\\cancer_training.csv",
            "Iris":"training\\iris_training.csv",
            "Wine":"training\\wine_training.csv",
            "Clase":"training\\clase_training.txt"
        }

        self.tecnicas = {
            "KNN":KNN,
            "NaiveBayes":"",
            "AsociadorLineal":"",
            "ID3":""
        }
        self.cbInstancia.addItems(self.instancias.keys())
        self.cbTecnica.addItems(self.tecnicas.keys())

        #New Window
        self.ardApp  = QtWidgets.QApplication(sys.argv)
        self.ardWindow = ard.MyApp()
       
	 
    #     #Instanciamos un objeto de la clase marduino
    #     self.arduino = ard.c_arduino()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execTimer)
        self.timer.start(10)
    #     self.teclado = Controller()
        

    def conectar(self):
        self.ardWindow.show()
        

    def identificar(self):
        #instancia y tecnica
        inst = self.cbInstancia.currentText()
        tec = self.cbTecnica.currentText()

        instArd = self.instancia_ard.text()
        instArd = instArd.split(",")


        #test = [int(x) for x in instArd]
        

        # #WINE
        #test = [[[13.48,1.67,2.64,22.5,89,2.6,1.1,0.52,2.29,11.75,0.57,1.78,620],3]]

        trainingFile = open(self.instancias[inst])
        trainContent = trainingFile.readlines()

        lista = [linea.split(",") for linea in trainContent]  #instancia wine
        #lista = [linea.split("\t") for linea in trainContent] #Instancia clase

        training = [ [ list(map(float,x[:len(lista[0])-1])), x[len(lista[0])-1].replace("\n","") ] for x in lista ]
        trainingFile.close()

        #Formato para el KNN [[caracteristicas],clase]
        #training = [ [ list(map(float,x[:len(lista[0])-1])), int(x[len(lista[0])-1].replace("\n","")) ] for x in lista ]

        # Instancia Clase
        #test = [[[23, 85, 84, 66, 1, 34]]]

        #instancia iris
        #test = [[[5.5,2.4,3.8,1.1]]]

        #instancia cancer 3,1,1,1,2,1,3,1,1,YES
        test = [[[3,1,1,1,2,1,3,1,1]]]



        self.tecnicas[tec](test,training)

   
    # def conectar(self):
    #     com = "COM"+self.txt_com.text()
    #     #print(com)
    #     # Inicializamos el arduino
    #     # Conexion a un puerto en LINUX /dev/tty
    #     # Enviar el COM que se ocupa en el dispositivo
    #     self.arduino.connect(com,self.btn_conectar)
    #     self.txt_com.setText("")
    #     if(self.arduino.verifyConnection()):
    #         # Si esta conectado...            
    #         self.txt_arduino.setEnabled(True)
    #         self.txt_arduino.setFocus()            
    #         self.beginRead()

    # def beginRead(self):
    #     if self.arduino == None:
    #         # Inicializar Conexion con Arduino
    #         self.conectar()
    #         print("Arduino Conectado")

    #     if not self.timer.isActive():
    #         self.timer.start(10)
    #     else:
    #         self.timer.stop()

    # # Timer para el Python
    def execTimer(self):
        lect = self.ardWindow.getLectura();
        self.instancia_ard.setText(lect)

    # def agregar(self):
    #     dato = self.txt_arduino.text()
    #     self.list_datos.addItem(dato)        
    #     self.txt_arduino.setText("")
    #     self.txt_arduino.setFocus() 


    def closeEvent(self, event):
        self.ardWindow.close()
        if self.timer.isActive():
            self.timer.stop()
        sys.exit(self.ardApp.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
