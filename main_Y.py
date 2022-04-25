import sys
import json
from PyQt5 import uic, QtWidgets, QtCore
import pandas as pd
# Modulo/clase arduino
import arduinoWind as ard
from techniques.KNN import KNN
from techniques.asociador_lineal import asociador_lineal as asolin
from techniques.naive_bayes import naive_bayes as naibay
import techniques.mapeador as mapea

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
        
        self.instancias, self.tecnicas, self.keyInst = self.read_yeison() 
        self.key = 0         
        self.instancia = self.instancias[self.keyInst[self.key]]                       

        archivo, delim, head, index = list(self.instancia.values())       
        self.dfDataset = mapea.leer_dataset(archivo, delim, eval(head), eval(index))      
        self.dfDsMap, self.discretizador = mapea.mapear_dataset(self.dfDataset)           
        
        self.tecnica = list(self.tecnicas.items())[0][0]   
        self.funcion = self.tecnicas[self.tecnica]
        
        self.cbInstancia.currentIndexChanged.connect(self.setInstancia)
        self.cbTecnica.currentIndexChanged.connect(self.setTecnica)

        # self.instancia_ard.setText("3, 2, 3, 1, 1, 2, 3, 1, 5") # DE YOCHUA

        # # Esto a mi no me funciono, me daba error (atte Yochua en Linux :v)
        # # New Window
        # self.ardApp  = QtWidgets.QApplication(sys.argv)
        # self.ardWindow = ard.MyApp()
       
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.execTimer)
        # self.timer.start(10)
    #     self.teclado = Controller()


    def read_yeison(self):
        nombreJSON = 'config.json'
        file = open(nombreJSON, 'r')
        data = json.load(file)
        file.close()

        instancias = data['instancias']
        tecnicas = data['tecnicas']
        key_instancias = list(instancias.keys())
        self.cbInstancia.addItems(instancias.keys())
        self.cbTecnica.addItems(tecnicas.keys())

        return instancias, tecnicas, key_instancias


    def conectar(self):
        self.ardWindow.show()
    

    def setInstancia(self):                
        self.key = self.cbInstancia.currentIndex()
        self.instancia = self.instancias[self.keyInst[self.key]] 

        archivo, delim, head, index = list(self.instancia.values())       
        self.dfDataset = mapea.leer_dataset(archivo, delim, eval(head), eval(index))      
        self.dfDsMap, self.discretizador = mapea.mapear_dataset(self.dfDataset) 
        print(self.dfDataset, "\n") 

        # a = [
        #     "3, 2, 3, 1, 1, 2, 3, 1, 5",
        #     "5.7, 3.2, 3, 1.7",
        #     "12, 1, 2.5, 22, 110, 3.1, 3, 0.32, 1.18, 7.69, 0.50, 2.22, 623",
        #     "56, 78, 90, 71, 47, 68"
        # ]
        # self.instancia_ard.setText(a[self.key])

        
    def setTecnica(self):        
        index = self.cbTecnica.currentIndex()
        self.tecnica = str(self.cbTecnica.itemText(index))
        self.funcion = self.tecnicas[self.tecnica]


    def identificar(self):
        print("\n----- {} -----".format(self.tecnica))
        text = (self.instancia_ard.text())
        vp = list(map(int, text.split(',')))                
        vpMap = self.mapearVP(vp)

        func = "{}({},{})".format(
            "eval(self.funcion)", "vpMap", "self.dfDsMap")             
        decision = eval(func)
        print(decision)


    def mapearVP(self, vpArduino):
        mins = self.dfDataset.min().to_list()
        maxs = self.dfDataset.max().to_list()
        
        vp = list(map(lambda x, y, z: round(x*(z-y)/1023+y, 4), vpArduino, mins, maxs ))
        
        dtipos = self.dfDataset.dtypes
        vpMap = mapea.discretizar_vp(vp, self.discretizador, dtipos)
        print("\nvp INO:      ",vpArduino)
        print("vp INO map:  ",vp)
        print("vp mapeado:  ",vpMap)
        print()       
        
        return vpMap


    # # Timer para el Python
    # def execTimer(self):
    #     lect = self.ardWindow.getLectura();
    #     self.instancia_ard.setText(lect)

    # Estos dos... el primero no se que era xd, y el segundo me daba error al cerrar la ventana xddd
    # def agregar(self):
    #     dato = self.txt_arduino.text()
    #     self.list_datos.addItem(dato)        
    #     self.txt_arduino.setText("")
    #     self.txt_arduino.setFocus() 


    # def closeEvent(self, event):
    #     self.ardWindow.close()
    #     if self.timer.isActive():
    #         self.timer.stop()
    #     sys.exit(self.ardApp.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
